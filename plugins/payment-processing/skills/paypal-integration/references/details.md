# paypal-integration — detailed patterns and worked examples

## REST Client (Orders v2)

```python
import time
import uuid
from decimal import Decimal

import requests


class PayPalClient:
    def __init__(self, client_id, client_secret, mode="sandbox"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = (
            "https://api-m.sandbox.paypal.com" if mode == "sandbox" else "https://api-m.paypal.com"
        )
        self._token = None
        self._token_expires_at = 0

    def access_token(self):
        """OAuth client-credentials token, cached until shortly before expiry."""
        if self._token and time.time() < self._token_expires_at - 60:
            return self._token
        response = requests.post(
            f"{self.base_url}/v1/oauth2/token",
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
            timeout=15,
        )
        response.raise_for_status()
        body = response.json()
        self._token = body["access_token"]
        self._token_expires_at = time.time() + body["expires_in"]
        return self._token

    def request(self, method, path, json=None, request_id=None):
        headers = {"Authorization": f"Bearer {self.access_token()}"}
        if request_id:
            # Idempotency: PayPal returns the original result if this ID is retried
            headers["PayPal-Request-Id"] = request_id
        return requests.request(
            method, f"{self.base_url}{path}", json=json, headers=headers, timeout=30
        )

    def create_order(self, amount: Decimal, currency="USD", request_id=None):
        """Create an order. `amount` must come from the server-side catalog."""
        response = self.request(
            "POST",
            "/v2/checkout/orders",
            json={
                "intent": "CAPTURE",
                "purchase_units": [
                    {"amount": {"currency_code": currency, "value": f"{amount:.2f}"}}
                ],
            },
            request_id=request_id or str(uuid.uuid4()),
        )
        response.raise_for_status()
        return response.json()

    def capture_order(self, order_id):
        """Capture an approved order.

        Returns the PayPal body on 422 (e.g. INSTRUMENT_DECLINED) so the caller
        can ask the buyer to pick another funding source.
        """
        response = self.request(
            "POST",
            f"/v2/checkout/orders/{order_id}/capture",
            json={},
            request_id=f"capture-{order_id}",  # retrying a capture never double-charges
        )
        if response.status_code != 422:
            response.raise_for_status()
        return response.json()

    def get_order(self, order_id):
        response = self.request("GET", f"/v2/checkout/orders/{order_id}")
        response.raise_for_status()
        return response.json()
```

Two-decimal formatting suits USD/EUR. Currencies like JPY take no decimals; check PayPal's currency codes table before adding one.

## Webhooks

Register the endpoint and the event types in the Developer Dashboard (or `POST /v1/notifications/webhooks`). Store the returned webhook ID as `PAYPAL_WEBHOOK_ID`.

Useful events for Orders v2:

- `PAYMENT.CAPTURE.COMPLETED` — money captured; fulfil here if the capture was `PENDING` at capture time
- `PAYMENT.CAPTURE.DENIED` — a pending capture failed
- `PAYMENT.CAPTURE.REFUNDED` / `PAYMENT.CAPTURE.REVERSED` — refund or reversal
- `CUSTOMER.DISPUTE.CREATED` — a dispute was opened

### Verified Webhook Handler

```python
import json
import os

from flask import Flask, request

app = Flask(__name__)
paypal = PayPalClient(os.environ["PAYPAL_CLIENT_ID"], os.environ["PAYPAL_CLIENT_SECRET"])


def verify_webhook(raw_body: str, headers) -> bool:
    """Ask PayPal to verify the signature (POST /v1/notifications/verify-webhook-signature)."""
    fields = {
        "auth_algo": headers["PAYPAL-AUTH-ALGO"],
        "cert_url": headers["PAYPAL-CERT-URL"],
        "transmission_id": headers["PAYPAL-TRANSMISSION-ID"],
        "transmission_sig": headers["PAYPAL-TRANSMISSION-SIG"],
        "transmission_time": headers["PAYPAL-TRANSMISSION-TIME"],
        "webhook_id": os.environ["PAYPAL_WEBHOOK_ID"],
    }
    # Splice the raw body in as-is: re-serialising the parsed event can change
    # key order or whitespace and make a genuine event fail verification.
    payload = json.dumps(fields)[:-1] + f', "webhook_event": {raw_body}}}'
    response = requests.post(
        f"{paypal.base_url}/v1/notifications/verify-webhook-signature",
        data=payload,
        headers={
            "Authorization": f"Bearer {paypal.access_token()}",
            "Content-Type": "application/json",
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["verification_status"] == "SUCCESS"


@app.post("/webhooks/paypal")
def paypal_webhook():
    raw_body = request.get_data(as_text=True)
    try:
        verified = verify_webhook(raw_body, request.headers)
    except KeyError:
        return "missing signature headers", 400
    if not verified:
        return "invalid signature", 400

    event = json.loads(raw_body)
    if already_processed(event["id"]):  # PayPal retries; dedupe on event id
        return "", 200

    # Enqueue and return fast; do slow work (DB, email, fulfilment) in a worker.
    enqueue_paypal_event(event)
    mark_processed(event["id"])
    return "", 200


def handle_paypal_event(event):
    """Runs in the worker."""
    resource = event["resource"]
    match event["event_type"]:
        case "PAYMENT.CAPTURE.COMPLETED":
            # resource is the capture; re-read it if you need authoritative state:
            # GET /v2/payments/captures/{resource["id"]}
            mark_order_paid_by_capture(resource["id"])
        case "PAYMENT.CAPTURE.DENIED":
            mark_order_failed_by_capture(resource["id"])
        case "PAYMENT.CAPTURE.REFUNDED" | "PAYMENT.CAPTURE.REVERSED":
            record_refund_or_reversal(resource)
        case "CUSTOMER.DISPUTE.CREATED":
            open_dispute_case(resource)
```

`verify-webhook-signature` adds a round trip per event. For high volume, verify offline instead: download the certificate from `cert_url` (only from a `paypal.com` host), and check the `PAYPAL-TRANSMISSION-SIG` signature over `transmission_id|transmission_time|webhook_id|crc32(raw_body)` with the `PAYPAL-AUTH-ALGO` algorithm. Events sent from the dashboard's webhook simulator can't be verified by either method.

## Subscription/Recurring Billing

The Subscriptions API lives under `/v1/billing/` and is current. Create a catalog product (`POST /v1/catalogs/products`) first, then a plan, then a subscription.

```python
def create_subscription_plan(client, product_id, name, amount: Decimal, currency="USD", interval="MONTH"):
    response = client.request(
        "POST",
        "/v1/billing/plans",
        json={
            "product_id": product_id,
            "name": name,
            "billing_cycles": [
                {
                    "frequency": {"interval_unit": interval, "interval_count": 1},
                    "tenure_type": "REGULAR",
                    "sequence": 1,
                    "total_cycles": 0,  # 0 = until cancelled
                    "pricing_scheme": {
                        "fixed_price": {"value": f"{amount:.2f}", "currency_code": currency}
                    },
                }
            ],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "payment_failure_threshold": 3,
            },
        },
        request_id=str(uuid.uuid4()),
    )
    response.raise_for_status()
    return response.json()


def create_subscription(client, plan_id, subscriber_email):
    """Returns the subscription ID and the URL to send the buyer to for approval."""
    response = client.request(
        "POST",
        "/v1/billing/subscriptions",
        json={
            "plan_id": plan_id,
            "subscriber": {"email_address": subscriber_email},
            "application_context": {
                "return_url": "https://yourdomain.com/subscription/success",
                "cancel_url": "https://yourdomain.com/subscription/cancel",
            },
        },
        request_id=str(uuid.uuid4()),
    )
    response.raise_for_status()
    subscription = response.json()
    approve = next(link["href"] for link in subscription["links"] if link["rel"] == "approve")
    return {"subscription_id": subscription["id"], "approval_url": approve}
```

Activate access on the `BILLING.SUBSCRIPTION.ACTIVATED` webhook, not on the return URL. Track renewals with `PAYMENT.SALE.COMPLETED` and failures with `BILLING.SUBSCRIPTION.PAYMENT.FAILED`.

## Refund Workflows

```python
def create_refund(client, capture_id, amount: Decimal | None = None, currency="USD", note=None):
    """Full refund when amount is None, partial otherwise."""
    payload = {}
    if amount is not None:
        payload["amount"] = {"value": f"{amount:.2f}", "currency_code": currency}
    if note:
        payload["note_to_payer"] = note

    response = client.request(
        "POST",
        f"/v2/payments/captures/{capture_id}/refund",
        json=payload,
        request_id=str(uuid.uuid4()),  # store and reuse this ID if you retry
    )
    response.raise_for_status()
    return response.json()


def get_refund(client, refund_id):
    response = client.request("GET", f"/v2/payments/refunds/{refund_id}")
    response.raise_for_status()
    return response.json()
```

## Error Handling

PayPal error bodies carry `name`, `details[].issue`, and `debug_id`. Log `debug_id` with every failure; PayPal support needs it.

```python
import logging

logger = logging.getLogger(__name__)

response = client.request("GET", f"/v2/checkout/orders/{order_id}")
if not response.ok:
    body = response.json()
    logger.error(
        "PayPal %s failed: %s %s (debug_id=%s)",
        "get_order",
        body.get("name"),
        [d.get("issue") for d in body.get("details", [])],
        body.get("debug_id"),
    )
    response.raise_for_status()
```

Retry only on network errors, 429, and 5xx, with backoff, and reuse the same `PayPal-Request-Id` so retries stay idempotent.

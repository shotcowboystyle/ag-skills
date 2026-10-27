---
name: paypal-integration
description: Integrate PayPal payment processing with server-side Orders v2 checkout, verified webhooks, subscriptions, and refunds. Use when implementing PayPal payments, processing online transactions, or building e-commerce checkout flows.
last_verified: 2026-10-27
---

# PayPal Integration

PayPal checkout on the Orders v2 REST API: the server creates and captures orders, the browser only renders buttons, and webhooks are verified before they are trusted.

## When to Use This Skill

- Integrating PayPal as a payment option
- Implementing PayPal Checkout (Smart Payment Buttons)
- Setting up recurring billing with PayPal Subscriptions
- Processing refunds and handling disputes
- Handling PayPal webhooks

## Core Rules

1. **The server sets the price.** The browser sends cart item IDs, never amounts. The server looks up prices and calls `POST /v2/checkout/orders`.
2. **The server captures.** The browser's `onApprove` calls your backend, which calls `POST /v2/checkout/orders/{id}/capture`. Never call `actions.order.create()` or `actions.order.capture()` in the browser: a buyer can edit the amount in DevTools.
3. **Check the capture, not just the order.** An order can be `COMPLETED` while its capture is `PENDING`. Fulfil on `purchase_units[0].payments.captures[0].status == "COMPLETED"` or on the `PAYMENT.CAPTURE.COMPLETED` webhook.
4. **Verify every webhook** with `POST /v1/notifications/verify-webhook-signature` before acting on it, and dedupe by event `id`.
5. **Use webhooks, not IPN.** IPN is the legacy notification system for classic NVP/SOAP integrations. Orders v2 integrations use webhooks.
6. **Don't use `paypalrestsdk`.** It targets the deprecated v1 Payments API and cannot capture a v2 order.

## Quick Start

```html
<!-- Frontend: JS SDK v5 buttons. v6 is PayPal's recommended SDK for new builds;
     the server endpoints below work unchanged with either. -->
<div id="paypal-button-container"></div>
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=USD"></script>
<script>
  paypal.Buttons({
    async createOrder() {
      const res = await fetch("/api/paypal/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cart: [{ sku: "PRO-PLAN", quantity: 1 }] }),
      });
      const order = await res.json();
      if (!order.id) throw new Error("Could not create order");
      return order.id;
    },
    async onApprove(data, actions) {
      const res = await fetch(`/api/paypal/orders/${data.orderID}/capture`, { method: "POST" });
      const result = await res.json();
      if (result.issue === "INSTRUMENT_DECLINED") return actions.restart();
      if (result.status !== "COMPLETED") throw new Error("Payment not completed");
      window.location.href = "/thank-you";
    },
  }).render("#paypal-button-container");
</script>
```

```python
# Backend (Flask). PayPalClient is defined in references/details.md.
import os
from decimal import Decimal  # never use floats for money
from flask import Flask, request, jsonify

app = Flask(__name__)
paypal = PayPalClient(
    os.environ["PAYPAL_CLIENT_ID"],
    os.environ["PAYPAL_CLIENT_SECRET"],
    mode=os.environ.get("PAYPAL_MODE", "sandbox"),
)

PRICES = {"PRO-PLAN": "25.00"}  # server-side catalog; load from your DB


@app.post("/api/paypal/orders")
def create_order():
    cart = request.get_json()["cart"]
    total = sum(Decimal(PRICES[item["sku"]]) * int(item["quantity"]) for item in cart)
    order = paypal.create_order(total, currency="USD")
    return jsonify({"id": order["id"]})


@app.post("/api/paypal/orders/<order_id>/capture")
def capture_order(order_id):
    result = paypal.capture_order(order_id)
    if result.get("details"):  # PayPal error body, e.g. INSTRUMENT_DECLINED
        return jsonify({"issue": result["details"][0]["issue"]}), 422

    capture = result["purchase_units"][0]["payments"]["captures"][0]
    if capture["status"] == "COMPLETED":
        mark_order_paid(order_id, capture_id=capture["id"])  # idempotent on capture_id
    # PENDING captures are resolved later by the PAYMENT.CAPTURE.* webhooks
    return jsonify({"status": capture["status"]})
```

## Detailed patterns and worked examples

`references/details.md` covers the `PayPalClient` (OAuth token caching, create/capture/get with `PayPal-Request-Id` idempotency), the verified webhook handler, subscriptions, and refunds.

## Testing

```python
# Sandbox credentials and test buyer/seller accounts come from developer.paypal.com.
import os
from decimal import Decimal

def test_create_order_sandbox():
    client = PayPalClient(
        os.environ["PAYPAL_SANDBOX_CLIENT_ID"],
        os.environ["PAYPAL_SANDBOX_CLIENT_SECRET"],
        mode="sandbox",
    )
    order = client.create_order(Decimal("10.00"))
    assert order["status"] == "CREATED"
    assert any(link["rel"] == "approve" for link in order["links"])
    # Approval needs a sandbox buyer in a browser; capture after that:
    # assert client.capture_order(order["id"])["status"] == "COMPLETED"
```

Use the Developer Dashboard's webhook simulator to send sample events. Simulator events can't be verified with `verify-webhook-signature`, so test verification with real sandbox transactions.

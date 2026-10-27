---
name: pci-compliance
description: Apply PCI DSS v4.0.1 to payment systems, with scope reduction first (hosted fields, processor tokens, SAQ A) and secure handling of whatever cardholder data remains. Use when securing payment processing, reducing PCI scope, or preparing for a PCI DSS assessment.
last_verified: 2026-10-27
---

# PCI Compliance

PCI DSS (Payment Card Industry Data Security Standard) v4.0.1 for systems that take card payments. The cheapest control is not touching card data at all: most applications should never see a PAN.

## When to Use This Skill

- Designing a checkout so card data never reaches your servers
- Choosing the right Self-Assessment Questionnaire (SAQ)
- Preparing for a PCI DSS assessment
- Reviewing code that logs, stores, or transmits payment data

## Version

PCI DSS v4.0.1 (June 2024) is the only active version. v3.2.1 retired on 31 March 2024 and v4.0 on 31 December 2024. The requirements v4.0 marked "best practice until 31 March 2025" are now mandatory.

## Scope Reduction First

Your PCI scope is every system that stores, processes, or transmits cardholder data, plus everything connected to those systems. Shrink it before you secure it:

1. **Let the processor collect the card.** Use a hosted payment page (Stripe Checkout, PayPal Checkout) or the processor's iframe fields (Stripe Payment Element, Braintree Hosted Fields). Card numbers go from the browser to the processor, never to you.
2. **Store processor tokens, not PANs.** Keep the processor's customer and payment-method IDs (`cus_...`, `pm_...`). They are useless outside your processor account.
3. **Need card data across processors?** Use a third-party network-token or vault service rather than building your own vault. A home-grown vault puts you in SAQ D scope.

| Integration | Card data path | Typical SAQ |
|---|---|---|
| Full redirect to hosted payment page | Browser to processor | SAQ A |
| Processor iframe fields embedded in your page | Browser to processor, inside the iframe | SAQ A |
| Your page's JavaScript reads or posts card data (direct post, JS-built form) | Your page handles the fields | SAQ A-EP |
| Card data reaches your servers | Your servers | SAQ D |

Your acquirer decides which SAQ applies. The eligibility criteria at the top of each SAQ are authoritative.

### E-commerce Page Scripts (v4.0.1)

Skimming attacks inject JavaScript into checkout pages. Two requirements target them:

- **6.4.3** — keep an inventory of every script on the payment page, with a written justification and a way to confirm each one is authorized and unaltered.
- **11.6.1** — detect unauthorized changes to the payment page's HTTP headers and contents, and alert on them.

The SAQ A revision of January 2025 removed 6.4.3 and 11.6.1 from SAQ A. It added an eligibility criterion instead: the merchant confirms its site is not susceptible to attacks from scripts that could affect its e-commerce systems. PCI SSC FAQ 1588 describes how to meet it. Iframe merchants usually still need script controls on the page hosting the iframe, or written confirmation from the provider. Full-redirect merchants are less exposed.

## The 12 Requirements (v4.0.1)

**Build and Maintain a Secure Network and Systems**

1. Install and maintain network security controls
2. Apply secure configurations to all system components

**Protect Account Data**

3. Protect stored account data
4. Protect cardholder data with strong cryptography during transmission over open, public networks

**Maintain a Vulnerability Management Program**

5. Protect all systems and networks from malicious software
6. Develop and maintain secure systems and software

**Implement Strong Access Control Measures**

7. Restrict access to system components and cardholder data by business need to know
8. Identify users and authenticate access to system components
9. Restrict physical access to cardholder data

**Regularly Monitor and Test Networks**

10. Log and monitor all access to system components and cardholder data
11. Test security of systems and networks regularly

**Maintain an Information Security Policy**

12. Support information security with organizational policies and programs

v4.0 changes that most often catch engineering teams:

- **8.4.2** — MFA for all access into the cardholder data environment, not only remote and admin access
- **8.3.6** — passwords of at least 12 characters (8 if the system can't support 12)
- **3.5.1.2** — disk or partition encryption alone no longer renders stored PAN unreadable on non-removable media
- **12.5.2** — confirm and document PCI scope at least once every 12 months
- **5.4.1** — automated anti-phishing controls

## Merchant Levels

Card brands set merchant levels, and your acquirer tells you which one applies and how you validate (SAQ or a Report on Compliance by a QSA). Visa's levels, by annual Visa transactions:

- **Level 1** — over 6 million (annual ROC)
- **Level 2** — 1 to 6 million
- **Level 3** — 20,000 to 1 million e-commerce
- **Level 4** — under 20,000 e-commerce, or up to 1 million total

Other brands use similar but not identical thresholds.

## Data You Must Never Store

Sensitive authentication data (SAD) must not be kept after authorization, even encrypted (requirement 3.3.1):

- Full track data (magnetic stripe or chip equivalent)
- Card verification code (CVV2/CVC2/CID)
- PIN or PIN block

PAN may be stored only if you have a business need, and then it must be unreadable (requirement 3.5.1). If you use a processor, you have no such need: store the token. If you truly must store PAN, read `references/details.md` first.

```python
PROHIBITED_FIELDS = {"cvv", "cvv2", "cvc", "cid", "pin", "pin_block", "track_data"}


class ProhibitedDataError(Exception):
    pass


def mask_pan(pan: str) -> str:
    """Display form: last four digits only."""
    return f"{'*' * (len(pan) - 4)}{pan[-4:]}"


def sanitize_for_log(data: dict) -> dict:
    """Strip SAD and mask any PAN before a dict reaches a log line."""
    clean = {k: v for k, v in data.items() if k.lower() not in PROHIBITED_FIELDS}
    if "card_number" in clean:
        clean["card_number"] = mask_pan(clean["card_number"])
    return clean


def assert_no_sad(record: dict) -> None:
    """Call before every write to storage."""
    found = PROHIBITED_FIELDS & {k.lower() for k in record}
    if found:
        raise ProhibitedDataError(f"refusing to store sensitive authentication data: {sorted(found)}")
```

## Tokenized Payments

The browser sends card details straight to the processor; your server only ever sees IDs.

```python
# Server: create a PaymentIntent and hand its client_secret to the browser.
import os
import stripe

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

intent = stripe.PaymentIntent.create(
    amount=2000,  # from your server-side price, in the smallest currency unit
    currency="usd",
    customer=customer_id,
    automatic_payment_methods={"enabled": True},
    setup_future_usage="off_session",  # save the card as a pm_... for later charges
)
# Return intent.client_secret to the browser.
```

```javascript
// Browser: Stripe's Payment Element iframe collects the card.
const elements = stripe.elements({ clientSecret });
elements.create("payment").mount("#payment-element");

const { error } = await stripe.confirmPayment({
  elements,
  confirmParams: { return_url: "https://yourdomain.com/complete" },
});
```

Store only `customer.id` and the `payment_method` ID. The `stripe-integration` skill covers the full flow, and the `paypal-integration` skill covers PayPal.

Do not use Stripe's legacy `createToken` / `Charge.create` / `Customer.modify(source=...)` APIs for new code. They don't handle SCA/3-D Secure.

## Data in Transit

Requirement 4.2.1 calls for strong cryptography on public networks: TLS 1.2 or later with secure cipher suites, and valid certificates. Terminate TLS at a load balancer or proxy you control, and set HSTS.

```python
# Flask session cookies for any page in scope
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)
```

## Additional patterns and templates

`references/details.md` covers storing PAN when you can't avoid it (KMS envelope encryption), access control, audit logging, SAQ selection, and a v4.0.1 checklist.

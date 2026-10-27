---
name: billing-automation
description: Build automated billing for recurring payments, invoicing, subscription lifecycle, proration, tax, and dunning, starting from a build-vs-buy decision and a billing provider such as Stripe Billing. Use when implementing subscription billing, automating invoicing, or managing recurring payment systems.
last_verified: 2026-10-27
---

# Billing Automation

Recurring billing: subscriptions, invoices, proration, tax, and failed-payment recovery (dunning). Decide whether to build or buy before writing any of it.

## When to Use This Skill

- Implementing SaaS subscription billing
- Automating invoice generation and delivery
- Managing failed payment recovery (dunning)
- Calculating prorated charges for plan changes
- Handling sales tax, VAT, and GST
- Processing usage-based billing

## Build vs Buy

Billing looks like a cron job and a `charge()` call. In practice it is calendar math, proration, tax registration and rates in many jurisdictions, card retries, SCA/3-D Secure, invoices that satisfy local law, revenue recognition, and an audit trail. Default to a provider.

**Buy** (Stripe Billing, Chargebee, Recurly, Maxio) when:

- Your plans fit fixed, per-seat, tiered, or metered pricing
- You want retries, dunning emails, a customer portal, and invoices without building them
- You already use the provider's payment processor

**Buy a merchant of record** (Paddle, Lemon Squeezy, FastSpring) when:

- You sell internationally and don't want to register for and remit sales tax/VAT yourself. The MoR is the legal seller and handles tax.

**Build** only when:

- Billing logic is your product (for example, a utility or telecom rating engine)
- Contracts are bespoke enough that no provider's model fits, and you have finance and tax people to own it
- You still pay a processor for the charge itself and a tax service for rates

Even when you build, don't hand-code tax rates. They change; use a tax engine (Stripe Tax, Avalara, Anrok, TaxJar).

## Core Concepts

### Subscription States (Stripe's names)

```
trialing → active → past_due → canceled | unpaid
incomplete → active | incomplete_expired
```

### Dunning

Recover failed renewals through smart retries, emails asking the customer to update their card, a grace period in `past_due`, and finally cancellation or `unpaid`.

### Proration

Credit unused time on the old price and charge remaining time on the new one when a customer upgrades, downgrades, or changes seat count mid-cycle.

## Quick Start (Stripe Billing)

```python
import os
import stripe

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# 1. Sign-up: Checkout collects the card and billing address (needed for tax).
session = stripe.checkout.Session.create(
    mode="subscription",
    line_items=[{"price": "price_pro_monthly", "quantity": 1}],  # Price created in Dashboard or API
    subscription_data={"trial_period_days": 14},
    automatic_tax={"enabled": True},  # requires Stripe Tax set up in the Dashboard
    success_url="https://yourdomain.com/billing/success?session_id={CHECKOUT_SESSION_ID}",
    cancel_url="https://yourdomain.com/pricing",
)
# Redirect the customer to session.url


# 2. Upgrade mid-cycle with proration.
def change_plan(subscription_id, new_price_id):
    subscription = stripe.Subscription.retrieve(subscription_id)
    return stripe.Subscription.modify(
        subscription_id,
        items=[{"id": subscription["items"]["data"][0]["id"], "price": new_price_id}],
        proration_behavior="create_prorations",
    )


# 3. Cancel at period end (customer keeps access until then).
stripe.Subscription.modify("sub_...", cancel_at_period_end=True)

# 4. Self-service: card updates, invoices, plan changes.
portal = stripe.billing_portal.Session.create(
    customer="cus_...", return_url="https://yourdomain.com/account"
)
```

Configure Smart Retries and failed-payment emails in the Dashboard's Billing settings. Drive access from webhooks, not from the success URL:

| Event | Action |
|---|---|
| `checkout.session.completed` | Link the new customer and subscription to your user |
| `customer.subscription.updated` | Sync `status`, plan, and period end; restrict access on `past_due`/`unpaid` |
| `customer.subscription.deleted` | Revoke access |
| `invoice.paid` | Extend access for the new period |
| `invoice.payment_failed` | Show an in-app "update your card" banner |

Webhook verification and idempotency are covered in the `stripe-integration` skill.

## Detailed patterns and worked examples

`references/details.md` has build-it-yourself sketches (lifecycle, cycle processing, dunning, proration, invoices, usage billing). Read it to understand what a provider does for you, or if you chose to build.

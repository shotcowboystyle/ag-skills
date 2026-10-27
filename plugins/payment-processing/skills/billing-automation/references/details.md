# billing-automation — detailed patterns and worked examples

These are sketches of what a billing provider does internally. They show the moving parts if you build; they are not a drop-in engine. Helpers such as `generate_id`, `get_subscription`, and `send_email` stand for your own persistence and email code. If you use Stripe Billing, Chargebee, or Recurly, most of this is configuration, not code.

## Subscription Lifecycle Management

```python
from datetime import datetime, timedelta
from enum import Enum

from dateutil.relativedelta import relativedelta  # pip install python-dateutil

class SubscriptionStatus(Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    PAUSED = "paused"

class Subscription:
    def __init__(self, customer_id, plan, billing_cycle_day=None):
        self.id = generate_id()
        self.customer_id = customer_id
        self.plan = plan
        self.status = SubscriptionStatus.TRIAL
        self.current_period_start = datetime.now()
        self.current_period_end = self.current_period_start + timedelta(days=plan.trial_days or 30)
        self.billing_cycle_day = billing_cycle_day or self.current_period_start.day
        self.trial_end = datetime.now() + timedelta(days=plan.trial_days) if plan.trial_days else None

    def start_trial(self, trial_days):
        """Start trial period."""
        self.status = SubscriptionStatus.TRIAL
        self.trial_end = datetime.now() + timedelta(days=trial_days)
        self.current_period_end = self.trial_end

    def activate(self):
        """Activate subscription after trial or immediately."""
        self.status = SubscriptionStatus.ACTIVE
        self.current_period_start = datetime.now()
        self.current_period_end = self.calculate_next_billing_date()

    def mark_past_due(self):
        """Mark subscription as past due after failed payment."""
        self.status = SubscriptionStatus.PAST_DUE
        # Trigger dunning workflow

    def cancel(self, at_period_end=True):
        """Cancel subscription."""
        if at_period_end:
            self.cancel_at_period_end = True
            # Will cancel when current period ends
        else:
            self.status = SubscriptionStatus.CANCELED
            self.canceled_at = datetime.now()

    def calculate_next_billing_date(self):
        """Calculate next billing date based on interval."""
        # Calendar months/years, not 30/365 days: Jan 31 + 1 month = Feb 28/29
        if self.plan.interval == 'month':
            return self.current_period_start + relativedelta(months=1)
        elif self.plan.interval == 'year':
            return self.current_period_start + relativedelta(years=1)
        elif self.plan.interval == 'week':
            return self.current_period_start + timedelta(weeks=1)
```

## Billing Cycle Processing

```python
class BillingEngine:
    def process_billing_cycle(self, subscription_id):
        """Process billing for a subscription."""
        subscription = self.get_subscription(subscription_id)

        # Check if billing is due
        if datetime.now() < subscription.current_period_end:
            return

        # Generate invoice
        invoice = self.generate_invoice(subscription)

        # Attempt payment
        payment_result = self.charge_customer(
            subscription.customer_id,
            invoice.total,
            invoice.id
        )

        if payment_result.success:
            # Payment successful
            invoice.mark_paid()
            subscription.advance_billing_period()
            self.send_invoice(invoice)
        else:
            # Payment failed
            subscription.mark_past_due()
            self.start_dunning_process(subscription, invoice)

    def generate_invoice(self, subscription):
        """Generate invoice for billing period."""
        invoice = Invoice(
            customer_id=subscription.customer_id,
            subscription_id=subscription.id,
            period_start=subscription.current_period_start,
            period_end=subscription.current_period_end
        )

        # Add subscription line item
        invoice.add_line_item(
            description=subscription.plan.name,
            amount=subscription.plan.amount,
            quantity=subscription.quantity or 1
        )

        # Add usage-based charges if applicable
        if subscription.has_usage_billing:
            usage_charges = self.calculate_usage_charges(subscription)
            invoice.add_line_item(
                description="Usage charges",
                amount=usage_charges
            )

        # Calculate tax
        tax = self.calculate_tax(invoice.subtotal, subscription.customer)
        invoice.tax = tax

        invoice.finalize()
        return invoice

    def charge_customer(self, customer_id, amount_cents: int, invoice_id):
        """Charge the customer's saved payment method off-session."""
        customer = self.get_customer(customer_id)

        try:
            intent = stripe.PaymentIntent.create(
                customer=customer.stripe_id,
                payment_method=customer.default_payment_method_id,
                amount=amount_cents,  # integer smallest currency unit, never float dollars
                currency='usd',
                off_session=True,
                confirm=True,
                idempotency_key=f"invoice-{invoice_id}",  # a retried job can't double-charge
            )
            return PaymentResult(success=intent.status == 'succeeded', transaction_id=intent.id)
        except stripe.CardError as e:
            # Declines and authentication_required (SCA) land here; both go to dunning.
            # On authentication_required, email the customer a link to confirm on-session.
            return PaymentResult(success=False, error=e.code)
```

## Dunning Management

```python
class DunningManager:
    """Manage failed payment recovery."""

    def __init__(self):
        self.retry_schedule = [
            {'days': 3, 'email_template': 'payment_failed_first'},
            {'days': 7, 'email_template': 'payment_failed_reminder'},
            {'days': 14, 'email_template': 'payment_failed_final'}
        ]

    def start_dunning_process(self, subscription, invoice):
        """Start dunning process for failed payment."""
        dunning_attempt = DunningAttempt(
            subscription_id=subscription.id,
            invoice_id=invoice.id,
            attempt_number=1,
            next_retry=datetime.now() + timedelta(days=3)
        )

        # Send initial failure notification
        self.send_dunning_email(subscription, 'payment_failed_first')

        # Schedule retries
        self.schedule_retries(dunning_attempt)

    def retry_payment(self, dunning_attempt):
        """Retry failed payment."""
        subscription = self.get_subscription(dunning_attempt.subscription_id)
        invoice = self.get_invoice(dunning_attempt.invoice_id)

        # Attempt payment again
        result = self.charge_customer(subscription.customer_id, invoice.total, invoice.id)

        if result.success:
            # Payment succeeded
            invoice.mark_paid()
            subscription.status = SubscriptionStatus.ACTIVE
            self.send_dunning_email(subscription, 'payment_recovered')
            dunning_attempt.mark_resolved()
        else:
            # Still failing
            dunning_attempt.attempt_number += 1

            if dunning_attempt.attempt_number < len(self.retry_schedule):
                # Schedule next retry
                next_retry_config = self.retry_schedule[dunning_attempt.attempt_number]
                dunning_attempt.next_retry = datetime.now() + timedelta(days=next_retry_config['days'])
                self.send_dunning_email(subscription, next_retry_config['email_template'])
            else:
                # Exhausted retries, cancel subscription
                subscription.cancel(at_period_end=False)
                self.send_dunning_email(subscription, 'subscription_canceled')

    def send_dunning_email(self, subscription, template):
        """Send dunning notification to customer."""
        customer = self.get_customer(subscription.customer_id)

        email_content = self.render_template(template, {
            'customer_name': customer.name,
            'amount_due': subscription.plan.amount,
            'update_payment_url': f"https://app.example.com/billing"
        })

        send_email(
            to=customer.email,
            subject=email_content['subject'],
            body=email_content['body']
        )
```

## Proration

```python
class ProrationCalculator:
    """Calculate prorated charges for plan changes."""

    @staticmethod
    def calculate_proration(old_plan, new_plan, period_start, period_end, change_date):
        """Calculate proration for plan change."""
        # Days in current period
        total_days = (period_end - period_start).days

        # Days used on old plan
        days_used = (change_date - period_start).days

        # Days remaining on new plan
        days_remaining = (period_end - change_date).days

        # Calculate prorated amounts
        unused_amount = (old_plan.amount / total_days) * days_remaining
        new_plan_amount = (new_plan.amount / total_days) * days_remaining

        # Net charge/credit
        proration = new_plan_amount - unused_amount

        return {
            'old_plan_credit': -unused_amount,
            'new_plan_charge': new_plan_amount,
            'net_proration': proration,
            'days_used': days_used,
            'days_remaining': days_remaining
        }

    @staticmethod
    def calculate_seat_proration(current_seats, new_seats, price_per_seat, period_start, period_end, change_date):
        """Calculate proration for seat changes."""
        total_days = (period_end - period_start).days
        days_remaining = (period_end - change_date).days

        # Additional seats charge
        additional_seats = new_seats - current_seats
        prorated_amount = (additional_seats * price_per_seat / total_days) * days_remaining

        return {
            'additional_seats': additional_seats,
            'prorated_charge': max(0, prorated_amount),  # No refund for removing seats mid-cycle
            'effective_date': change_date
        }
```

## Tax Calculation

Don't hard-code tax rates. They differ by state, county, city, and product type, they change, and you only owe tax where you are registered or have nexus. Call a tax engine per invoice with the customer's address and your product tax code:

- Stripe Tax (`automatic_tax={"enabled": True}` on Checkout, Subscriptions, and Invoices)
- Avalara, Anrok, TaxJar, or Vertex via their APIs
- A merchant of record (Paddle, Lemon Squeezy) if you want them to be the seller and remit tax for you

```python
# Stripe Tax on a one-off calculation, e.g. to show tax before checkout
calculation = stripe.tax.Calculation.create(
    currency="usd",
    line_items=[{"amount": 2000, "reference": "pro_monthly", "tax_code": "txcd_10103001"}],  # SaaS
    customer_details={
        "address": {"line1": "510 Townsend St", "city": "San Francisco", "state": "CA",
                    "postal_code": "94103", "country": "US"},
        "address_source": "billing",
    },
)
tax_cents = calculation.tax_amount_exclusive
```

For EU B2B reverse charge, validate the customer's VAT number (VIES) and pass it as a customer tax ID so the engine applies reverse charge.

## Invoice Generation

```python
class Invoice:
    def __init__(self, customer_id, subscription_id=None):
        self.id = generate_invoice_number()
        self.customer_id = customer_id
        self.subscription_id = subscription_id
        self.status = 'draft'
        self.line_items = []
        self.subtotal = 0
        self.tax = 0
        self.total = 0
        self.created_at = datetime.now()

    def add_line_item(self, description, amount, quantity=1):
        """Add line item to invoice."""
        line_item = {
            'description': description,
            'unit_amount': amount,
            'quantity': quantity,
            'total': amount * quantity
        }
        self.line_items.append(line_item)
        self.subtotal += line_item['total']

    def finalize(self):
        """Finalize invoice and calculate total."""
        self.total = self.subtotal + self.tax
        self.status = 'open'
        self.finalized_at = datetime.now()

    def mark_paid(self):
        """Mark invoice as paid."""
        self.status = 'paid'
        self.paid_at = datetime.now()

    def to_pdf(self):
        """Generate PDF invoice."""
        from reportlab.pdfgen import canvas

        # Generate PDF
        # Include: company info, customer info, line items, tax, total
        pass

    def to_html(self):
        """Generate HTML invoice."""
        template = """
        <!DOCTYPE html>
        <html>
        <head><title>Invoice #{invoice_number}</title></head>
        <body>
            <h1>Invoice #{invoice_number}</h1>
            <p>Date: {date}</p>
            <h2>Bill To:</h2>
            <p>{customer_name}<br>{customer_address}</p>
            <table>
                <tr><th>Description</th><th>Quantity</th><th>Amount</th></tr>
                {line_items}
            </table>
            <p>Subtotal: ${subtotal}</p>
            <p>Tax: ${tax}</p>
            <h3>Total: ${total}</h3>
        </body>
        </html>
        """

        return template.format(
            invoice_number=self.id,
            date=self.created_at.strftime('%Y-%m-%d'),
            customer_name=self.customer.name,
            customer_address=self.customer.address,
            line_items=self.render_line_items(),
            subtotal=self.subtotal,
            tax=self.tax,
            total=self.total
        )
```

## Usage-Based Billing

```python
class UsageBillingEngine:
    """Track and bill for usage."""

    def track_usage(self, customer_id, metric, quantity):
        """Track usage event."""
        UsageRecord.create(
            customer_id=customer_id,
            metric=metric,
            quantity=quantity,
            timestamp=datetime.now()
        )

    def calculate_usage_charges(self, subscription, period_start, period_end):
        """Calculate charges for usage in billing period."""
        usage_records = UsageRecord.get_for_period(
            subscription.customer_id,
            period_start,
            period_end
        )

        total_usage = sum(record.quantity for record in usage_records)

        # Tiered pricing
        if subscription.plan.pricing_model == 'tiered':
            charge = self.calculate_tiered_pricing(total_usage, subscription.plan.tiers)
        # Per-unit pricing
        elif subscription.plan.pricing_model == 'per_unit':
            charge = total_usage * subscription.plan.unit_price
        # Volume pricing
        elif subscription.plan.pricing_model == 'volume':
            charge = self.calculate_volume_pricing(total_usage, subscription.plan.tiers)

        return charge

    def calculate_tiered_pricing(self, total_usage, tiers):
        """Calculate cost using tiered pricing."""
        charge = 0
        remaining = total_usage

        for tier in sorted(tiers, key=lambda x: x['up_to']):
            tier_usage = min(remaining, tier['up_to'] - tier['from'])
            charge += tier_usage * tier['unit_price']
            remaining -= tier_usage

            if remaining <= 0:
                break

        return charge
```

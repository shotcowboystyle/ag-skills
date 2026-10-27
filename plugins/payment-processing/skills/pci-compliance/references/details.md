# pci-compliance — additional patterns and templates

## If You Must Store PAN

That puts you in SAQ D or ROC territory. Before building it, confirm with your QSA. The minimum:

- **Encryption keys live in a KMS or HSM** (AWS KMS, Google Cloud KMS, Azure Key Vault, an HSM). Use envelope encryption: a data key per record or batch, wrapped by a KMS key that never leaves the KMS. Never generate a key in application code at startup, and never put one in an environment variable or source.
- **Keys are rotated** on a defined cryptoperiod and access to them is logged (requirements 3.6 and 3.7).
- **A keyed hash** (HMAC with a KMS-held key), not a plain hash, if you need to look up or deduplicate PANs (requirement 3.5.1.1).
- **Decryption is a separate, tightly permissioned service**, not something every app server can do.

## Access Control

```python
from functools import wraps
from flask import session

def require_pci_access(f):
    """Decorator to restrict access to cardholder data."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get('user')

        # Check if user has PCI access role
        if not user or 'pci_access' not in user.get('roles', []):
            return {'error': 'Unauthorized access to cardholder data'}, 403

        # Log access attempt
        audit_log(
            user=user['id'],
            action='access_cardholder_data',
            resource=f.__name__
        )

        return f(*args, **kwargs)

    return decorated_function

@app.route('/api/payment-methods')
@require_pci_access
def get_payment_methods():
    """Retrieve payment methods (restricted access)."""
    # Only accessible to users with pci_access role
    pass
```

## Audit Logging

Requirement 10 wants every access to cardholder data and every authentication event logged with who, what, when, where from, and the outcome. Ship logs off the host to append-only storage, and never log PAN or SAD.

```python
import json
import logging
from datetime import datetime, timezone

from flask import request


class PCIAuditLogger:
    def __init__(self):
        # Route this logger to a write-once sink (e.g. SIEM or object-lock bucket).
        self.logger = logging.getLogger("pci_audit")

    def _write(self, entry):
        entry["timestamp"] = datetime.now(timezone.utc).isoformat()
        entry["ip_address"] = request.remote_addr
        self.logger.info(json.dumps(entry))

    def log_access(self, user_id, resource, action, result):
        self._write(
            {"user_id": user_id, "resource": resource, "action": action, "result": result}
        )

    def log_authentication(self, user_id, success, method):
        self._write(
            {"user_id": user_id, "event": "authentication", "success": success, "method": method}
        )


audit = PCIAuditLogger()
audit.log_access(user_id=123, resource="payment_methods", action="read", result="success")
```

Keep audit logs for at least 12 months, with the last three months immediately available (requirement 10.5.1).

## SAQ Selection

The SAQ depends on how card data flows, not on company size. Your acquirer confirms which one you file.

### SAQ A

- Card-not-present merchant; all card data functions outsourced to PCI DSS compliant providers
- Payment page is a full redirect or the provider's iframe
- No electronic storage, processing, or transmission of card data on your systems
- Must meet the eligibility criterion that the site is not susceptible to script attacks (January 2025 revision)

### SAQ A-EP

- E-commerce where your page controls how card data reaches the processor (direct post, JavaScript-built fields), but your servers never receive it
- Includes most of requirements 6 and 11 for the web servers that serve the payment page, including 6.4.3 and 11.6.1

### SAQ D

- Anything that stores, processes, or transmits card data on your systems, or that doesn't fit another SAQ
- Covers all PCI DSS requirements; there are separate SAQ D versions for merchants and service providers

Other SAQs (B, B-IP, C, C-VT, P2PE, SPoC) cover card-present terminals and virtual terminals.

## Compliance Checklist (v4.0.1)

```python
PCI_COMPLIANCE_CHECKLIST = {
    "scope": [
        "Cardholder data flows documented",
        "Scope confirmed and documented in the last 12 months (12.5.2)",
        "Network segmentation isolates the cardholder data environment",
    ],
    "secure_network_and_systems": [
        "Network security controls configured and reviewed (Req 1)",
        "Vendor default accounts disabled or passwords changed (Req 2)",
    ],
    "account_data": [
        "No sensitive authentication data stored after authorization (3.3.1)",
        "Stored PAN unreadable; keys in KMS/HSM and rotated (3.5, 3.6, 3.7)",
        "PAN masked when displayed (3.4.1)",
        "TLS 1.2+ with valid certificates on public networks (4.2.1)",
    ],
    "vulnerability_management": [
        "Anti-malware and anti-phishing controls (Req 5, 5.4.1)",
        "Secure development, patching, and code review (Req 6)",
        "Payment page script inventory and integrity checks (6.4.3)",
    ],
    "access_control": [
        "Access restricted by need to know (Req 7)",
        "Unique IDs; MFA for all access into the CDE (8.4.2)",
        "Passwords at least 12 characters (8.3.6)",
        "Physical access controls (Req 9)",
    ],
    "monitoring_and_testing": [
        "Audit logs collected, reviewed, retained 12 months (Req 10)",
        "Quarterly internal and external vulnerability scans (11.3)",
        "Payment page change and tamper detection (11.6.1)",
    ],
    "policy": [
        "Information security policy reviewed annually (Req 12)",
        "Targeted risk analyses where requirements allow flexibility (12.3.1)",
        "Security awareness training",
        "Incident response plan tested",
    ],
}
```

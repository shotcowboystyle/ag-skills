# email-deliverability

DNS planning, auditing, and verification for email on any domain, DNS host, and mail provider.

## Skill

- `email-dns-setup`: produces a complete record set (MX, SPF, DKIM, DMARC with a staged rollout, MTA-STS, TLS-RPT, BIMI), explains subdomain strategy for several domains or senders, locks down domains that never send, and verifies the published records. Provider values come from the provider's docs or portal, never from memory.

## What is inside

```
skills/email-dns-setup/
├── SKILL.md
├── references/   # records, providers, DNS hosts, architecture, answer checklist
├── scripts/check_mail_dns.sh   # live DNS verification with dig
└── evals/evals.json
```

## Installation

```bash
/plugin marketplace add shotcowboystyle/ag-skills
/plugin install email-deliverability@claude-code-workflows
```

## Requirements

- `dig` on PATH for `scripts/check_mail_dns.sh`.

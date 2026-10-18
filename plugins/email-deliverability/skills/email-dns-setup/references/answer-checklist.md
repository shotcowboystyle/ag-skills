# Answer checklist

Read this before writing the final answer. It holds the best practices every answer states, the
pitfalls to check the record set against, and the output template.

## Best practices to state every time

Include these in every response, briefly, even when the user only asked for records. They are the
difference between "mail works today" and "mail still works in a year".

- **Registrar hygiene**: 2FA, auto-renew, registrar/transfer lock. An expired domain hands every
  password-reset email to whoever buys it.
- **DNS host hygiene**: 2FA, and if a provider offers an "account reset via DNS" feature, enable it
  on one domain only, the most locked-down one.
- **Short TTLs during migration** (300), raise to 3600 or higher once stable.
- **SPF ends in `-all` or `~all`, never `+all`.** Prefer `-all` once DMARC reports show nothing
  unexpected; `~all` is fine during migration.
- **No catch-all** mailbox; use explicit aliases and plus-addressing. Catch-alls collect spam and
  make it impossible to retire an address.
- **One mailbox per business or brand** so it can be handed off or sold without untangling.
- **Keep records in version control** if the user already manages infrastructure as code, but keep
  automated tools (external-dns, cert-manager) scoped so they cannot delete hand-managed mail records.
- **Re-check after any provider change**, because old DKIM selectors keep validating until removed
  and old SPF includes keep authorizing a service the user no longer uses.

## Pitfalls that cause most tickets

- Cloudflare (or any proxying host) proxying DKIM/MX/autodiscover CNAMEs. They must be "DNS only".
- Apex CNAME. Most hosts forbid it; those that allow it (CNAME flattening, ALIAS) break MX at the
  apex. Mail records stay as plain MX/TXT.
- TXT strings over 255 characters (2048-bit DKIM keys): split into multiple quoted strings in one
  record, or use the provider's CNAME form. Details in `references/records.md`.
- Host UI auto-appending the zone, producing `_dmarc.example.com.example.com`. Check with `dig`.
- SPF with more than 10 lookups (`permerror`, treated as no SPF). Use subdomains per sender, or a
  flattening service, never a second SPF record.
- Forgetting the deletion list when migrating providers.
- DMARC `rua=` pointing at a different domain without the external authorization record
  (`example.com._report._dmarc.reports-domain.com TXT "v=DMARC1"`) on the receiving side.
- Subdomains without their own DMARC inherit the org policy via `sp=`; set `sp=` deliberately.

## Output template

```
## Mail DNS plan for <domain>

**Roles**: people mail on `<domain>` via <provider>; transactional on `notify.<domain>` via <service>; ...
**DNS host**: <host> (confirmed via NS). **Registrar**: <registrar>. **Managed by**: <hand | tofu | external-dns>.

### Records to add — <zone>
<table>

### Records to delete
- ...

### Entering these at <host>
- ...

### Mailbox-side setup
- ...

### Verify
1. ...

### DMARC rollout
- Now: p=none; rua -> ... ; alignment adkim=r/aspf=r because <sending subdomains | strict because only apex sends>; review reports <date>.
- Then: p=quarantine (pct=25 then 100); then p=reject; set sp= explicitly for subdomains.

### Hygiene checklist
- [ ] registrar 2FA + auto-renew + lock  - [ ] DNS host 2FA  - [ ] postmaster@/abuse@/dmarc@ exist  - [ ] ...
```

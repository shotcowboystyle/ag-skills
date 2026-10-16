---
name: email-dns-setup
description: Plan, generate, audit and verify the DNS records that make email work and keep it out of spam for any domain, on any registrar or DNS host (Cloudflare, Route 53, Namecheap, GoDaddy, Porkbun, Vercel, Google Domains/Squarespace, DigitalOcean, OpenTofu/Terraform, external-dns, etc.) and any mail service (Google Workspace, Microsoft 365, Fastmail, Proton, iCloud, Zoho, Purelymail, Migadu, mailcow/Stalwart/Postfix self-hosted, plus Postmark/SES/Resend/SendGrid/Mailgun/Mailchimp senders). Covers MX, SPF, DKIM, DMARC, MTA-STS, TLS-RPT, BIMI, autodiscover, subdomain strategy, and locking down domains that never send. Use this whenever the user mentions MX/SPF/DKIM/DMARC, "email DNS", setting up email on a domain, moving mail providers, adding a newsletter or transactional sender, "emails going to spam", "mail not arriving", DMARC reports, or asks how to structure mail for several domains or side businesses, even if they only say "set up email for mydomain.com".
---

# Email DNS setup

Email deliverability is mostly DNS. One wrong or missing record and mail silently lands in spam, or
anyone can send as the domain. This skill produces a correct, complete record set for a domain,
explains the architecture choices, and verifies the result. It is provider-agnostic: provider-specific
values (MX hosts, DKIM selectors, SPF includes) come from the provider's own documentation or portal,
never from memory, because they change and a stale selector is a silent failure.

## Workflow

### 1. Gather context (ask only for what you cannot look up)

Collect these before generating records. Look up what you can with the audit script in step 2 and
ask the user for the rest in one message.

- **Domain(s)** and what each one is for: people's mailboxes, app/transactional mail, newsletters,
  parked / never sends.
- **Mailbox provider** (where humans read mail), if any.
- **Other senders**: transactional service, marketing platform, CRM, helpdesk, website contact form,
  anything else that puts the domain in a From header. Each needs SPF and DKIM authorization.
- **DNS host** (where the nameservers point) and **registrar** (where the domain is renewed). They are
  often different. Run `dig NS` to confirm the DNS host rather than trusting the registrar name.
- **How DNS is managed**: by hand in a dashboard, OpenTofu/Terraform, external-dns, a provider CLI/API.
  This changes where the records should live so automation does not fight manual entries.
- **Existing mail** on the domain: migrating from another provider means the old MX/SPF/DKIM must be
  removed, not added to.

### 2. Audit the current state

Run the bundled script first. It is read-only and shows exactly what the world sees right now.

```bash
scripts/check_mail_dns.sh example.com [dkim-selector ...]
```

It reports NS, MX, SPF (with the DNS lookup count against the limit of 10), DKIM for any selectors
you pass plus a list of common ones, DMARC, MTA-STS, TLS-RPT and BIMI, and flags the usual
problems: multiple SPF records, `+all`, missing DMARC, DMARC without `rua=`, a CNAME on the apex.
Needs `dig` (bind-tools / dnsutils). Point it at the authoritative server with `NS=ns1.example.net`
right after a change, before caches update, or at a public resolver with `RESOLVER=1.1.1.1` when
the local resolver truncates big TXT sets or hangs (some networks block TCP 53).

### 3. Decide the architecture

Settle these with the user, then write them down in the output. Read
[references/architecture.md](references/architecture.md) when a question goes beyond the summary below.

- **People use the root domain.** `you@business.com` is what customers expect. `you@mail.business.com`
  looks wrong and gains nothing. (Terminology: the "TLD" is only `.com`; the thing being configured is
  the root or apex domain.)
- **Automated mail uses dedicated subdomains**, each through a service built for it: `news.` or `mail.`
  for marketing, `notify.`, `tx.` or `send.` for transactional. Reputation is tracked per domain, so
  a newsletter complaint spike does not take password-reset mail down with it, and the root domain's
  SPF record stays short.
- **Do not send bulk or app mail through the mailbox provider.** Mailbox providers rate-limit and
  are not built for bounce handling. Transactional services are.
- **One SPF record per name.** Two `v=spf1` TXT records at the same name is a permanent SPF failure.
  Merge includes into one record and stay under 10 DNS-querying mechanisms.
- **Own the DMARC record.** Some providers offer a CNAME to their DMARC policy. Decline it: it skips
  the reporting phase and often starts at `p=reject`, so mail from any forgotten sender is dropped
  with no visibility. Publish a TXT record with `p=none` and an `rua=` address the user actually
  reads, then tighten. Rollout plan is in [references/records.md](references/records.md#dmarc).
- **Lock down domains that never send.** A parked domain with no mail records is a free phishing
  domain. Publish null MX, `v=spf1 -all`, `p=reject` DMARC and an empty wildcard DKIM.
- **Add the newer protections** when the provider supports them: MTA-STS and TLS-RPT for transport
  encryption, BIMI only after DMARC is at enforcement (and it needs a VMC for most receivers).

### 4. Generate the record set

Get provider values from [references/providers.md](references/providers.md) for the common
providers, or from the provider's current docs / admin portal for anything else. When a value
(DKIM selector, verification token, MX priority) comes from the user's portal, leave a clear
placeholder like `<from Purelymail portal>` rather than inventing one. Record syntax, length limits
and quoting rules are in [references/records.md](references/records.md).

Present records in this exact table shape, one table per zone, so they can be pasted into any host:

| Host (relative) | Type | Priority | Value | TTL | Notes |
|---|---|---|---|---|---|
| `@` | MX | 10 | `mx.provider.example.` | 3600 | |
| `@` | TXT | | `v=spf1 include:_spf.provider.example -all` | 3600 | only SPF record on `@` |
| `sel1._domainkey` | CNAME | | `sel1.dkim.provider.example.` | 3600 | DNS only, never proxied |
| `_dmarc` | TXT | | `v=DMARC1; p=none; rua=mailto:dmarc@example.com` | 3600 | tighten after 2 to 4 weeks |

Then give, separately:

1. **Records to delete** (old MX, old SPF, old DKIM, duplicate TXT). Deletions are the step people
   skip and the most common cause of "I added everything and it still fails".
2. **Host-specific entry notes** from [references/dns-hosts.md](references/dns-hosts.md): how this
   host writes the apex (`@` vs blank vs full name), whether it auto-appends the zone, TXT quoting,
   proxy toggles, API/IaC snippets if the user manages DNS as code.
3. **Mailbox-side setup** the DNS cannot do: create `postmaster@`, `abuse@` (RFC 2142) and the
   `dmarc@` report address, role aliases (`hello@`, `support@`, `billing@`), 2FA, app passwords.
4. **Verification steps** (step 5).

Use the full output template at the end of this file.

### 5. Verify

1. Re-run `scripts/check_mail_dns.sh` with the DKIM selectors. Everything the table says should be
   visible. If not, check the authoritative server directly (`NS=`) to separate "not published" from
   "not propagated yet". In the answer you give the user, write out plain `dig` commands (the list
   in references/records.md) rather than naming this script: the user usually does not have the
   skill's files, and a command they cannot run is worse than none. Offer to re-run the audit for
   them instead.
2. Send a message from the new setup to a Gmail or Outlook.com mailbox and open "Show original" /
   "View message source". SPF, DKIM and DMARC must all show PASS, and the DKIM `d=` must be the
   user's domain, not the provider's. A provider-domain `d=` means the DKIM CNAMEs are wrong or
   proxied.
3. For transactional and marketing subdomains, trigger a real send from the service and check the
   same headers.
4. Optionally use mail-tester.com, MXToolbox or Learn and Test DMARC for a third-party read.
5. Set a reminder to review the first DMARC aggregate reports in two weeks and move to
   `p=quarantine`, then `p=reject`. Cloudflare DMARC Management, Postmark's free DMARC digest, or
   dmarcian parse the XML; raw reports are unreadable by hand.

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
  record, or use the provider's CNAME form. Details in references/records.md.
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
- Now: p=none, rua -> ... ; review reports <date>.
- Then: p=quarantine; then p=reject.

### Hygiene checklist
- [ ] registrar 2FA + auto-renew + lock  - [ ] DNS host 2FA  - [ ] postmaster@/abuse@/dmarc@ exist  - [ ] ...
```

## Reference files

- [references/records.md](references/records.md): every record type, exact syntax, limits, DMARC rollout, MTA-STS/TLS-RPT/BIMI, null-MX lockdown.
- [references/providers.md](references/providers.md): record templates and doc links for mailbox providers, transactional and marketing senders, self-hosted servers.
- [references/dns-hosts.md](references/dns-hosts.md): per-host UI quirks, CLI/API examples, OpenTofu/Terraform and external-dns guidance.
- [references/architecture.md](references/architecture.md): root vs subdomain reasoning, multi-domain/multi-business layouts, migration sequencing, forwarding and ARC.
- `scripts/check_mail_dns.sh`: read-only audit of a domain's mail DNS.

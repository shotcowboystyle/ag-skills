# Mail architecture decisions

Contents: [Root vs subdomain](#root-domain-vs-subdomain) · [Sender separation](#one-service-per-job) ·
[Many domains / side businesses](#several-domains-or-side-businesses) · [Migration sequencing](#migrating-between-providers) ·
[Forwarding, ARC, mailing lists](#forwarding-arc-and-mailing-lists) · [Self-hosting](#self-hosting-considerations) ·
[Account-level security](#account-level-security)

## Root domain vs subdomain

Reputation at Gmail, Microsoft and Yahoo is tracked per *organizational domain and per sending
subdomain* together with the sending IP and the DKIM `d=` value. Separation therefore buys
isolation, but only where the mail stream is genuinely different.

| Mail stream | Name | Why |
|---|---|---|
| People (staff, founders, support replies) | `example.com` | It is the brand; anything else looks like phishing to recipients |
| Transactional (receipts, resets, alerts, contact-form relays) | `notify.example.com`, `tx.`, `send.`, `mail.` | High volume, machine-generated, must never be throttled by a newsletter complaint spike |
| Marketing / newsletters | `news.example.com`, `email.`, `hello.` | Highest complaint rate; isolate it |
| Self-hosted server hostname | `mail.example.com` / `mx.example.com` | Needs its own A/AAAA, PTR, SPF for HELO; not used in addresses |
| Nothing | parked domains | Null MX + reject (records.md) |

The From address on transactional mail can still read `support@example.com` style only if the
service signs with a `d=` that aligns: either `d=example.com` (DKIM key for the root on the
service) or `d=notify.example.com` with relaxed alignment (`adkim=r`, the DMARC default). Relaxed
alignment is what makes the subdomain layout work without ugly From addresses, so do not set
`adkim=s` on a domain that uses sending subdomains.

With a hosted mailbox provider, `mail.example.com` is not needed at all. Hosts like Cloudflare
sometimes pre-create `mail` A records pointing at the web server; delete them so nobody is
tempted to use them.

## One service per job

- Mailbox provider: humans only. They rate-limit outbound (Google Workspace 2,000/day, Microsoft
  365 10,000 recipients/day, most small providers far less) and treat bulk sending as abuse.
- Transactional service (Postmark, Amazon SES, Resend, SendGrid, Mailgun, Brevo, Mailjet, SparkPost,
  Loops for product email): handles bounces, complaints, suppression lists, webhooks. Give each app
  or environment its own sending subdomain or at least its own stream.
- Marketing platform (Mailchimp, Kit, Beehiiv, Klaviyo, Customer.io, Buttondown, HubSpot): has its
  own list management and unsubscribe handling, which Gmail/Yahoo bulk-sender rules now require
  (one-click `List-Unsubscribe`, complaint rate under 0.3%).
- Helpdesk / CRM (Zendesk, Front, HubSpot, Intercom, Help Scout): often sends *as* the root domain
  on behalf of staff. Each of these needs its own DKIM selectors on the root domain and an SPF
  include if it uses its own return-path on the root; count the lookups.

A domain with people mail plus two or three such services usually ends up with 5 to 9 DKIM
CNAMEs and a 4 to 7 lookup SPF on the root. That is normal. Past that, push services to
subdomains.

## Several domains or side businesses

Common for solo founders and agencies. Guidance that keeps it manageable:

- One mailbox (or one mailbox provider account) per business; aliases and routing rules for role
  addresses. A business that gets sold or handed off then moves with its mailbox.
- Same record pattern on every domain, differing only in the DKIM selectors/tokens the provider
  issues per domain. Generate the record tables per zone and keep them in a single doc or repo.
- One DMARC report mailbox for all domains (`dmarc@primary.example`) is fine, but each *other*
  domain then needs the `_report._dmarc` authorization record on `primary.example`, or use a
  hosted DMARC service that handles it.
- Pick one domain as the "identity anchor" (the registrar/mail-provider account recovery address
  lives there) and give it the strictest settings: registrar lock, `-all`, `p=reject`, no catch-all,
  mailbox 2FA with hardware keys if available. Compromise of that domain's DNS is compromise of
  every account recovered through it.
- Brand-protection domains (typos, other TLDs) that only redirect get the null-MX lockdown.
- Keep `postmaster@` and `abuse@` working on every domain that has MX (RFC 2142). Providers and
  blocklist operators write to them; a bounce there looks like an abandoned domain.

## Migrating between providers

Order matters because MX, DKIM and SPF changes propagate at different rates and the old
provider keeps receiving for a while.

1. Lower TTLs on the records that will change to 300 at least 24 h before (after the current
   TTL has expired).
2. Create mailboxes and aliases at the new provider; verify domain ownership (usually a TXT
   token, sometimes a CNAME).
3. Add the new DKIM selectors alongside the old ones. Both providers can now sign.
4. Add the new provider's SPF include to the *same* record as the old one (temporarily longer SPF).
5. Migrate mail data (IMAP sync tools, provider import).
6. Switch MX to the new provider. Mail now arrives at the new mailboxes; the old provider
   continues to receive whatever stragglers hit cached MX for up to the old TTL.
7. Switch users' clients; send test mail; confirm headers.
8. After one to two weeks: remove the old SPF include, old DKIM selectors, old verification TXT,
   old autodiscover records. Raise TTLs back.
9. Close the old account only after confirming nothing still delivers there.

Moving a transactional or marketing sender follows the same shape on its subdomain, and can be
done independently of the mailbox migration.

## Forwarding, ARC, and mailing lists

Forwarding breaks SPF (the forwarder's IP is not in the original domain's SPF) and sometimes DKIM
(if the forwarder rewrites the body or subject). With DMARC at `p=reject`, forwarded mail to a
Gmail user can be dropped. Mitigations:

- Prefer provider-native forwarding/routing rules (they use SRS to rewrite the envelope sender).
- Make sure DKIM is published and the provider signs the body in a way that survives forwarding
  (relaxed/relaxed canonicalization, which is the default everywhere that matters).
- Large receivers honor ARC (Authenticated Received Chain) from known forwarders, which is why
  Gmail-to-Gmail forwarding keeps working.
- Mailing lists (Google Groups, Mailman) rewrite From when the sender's domain is at `p=reject`;
  this is expected behaviour, not a misconfiguration.

## Self-hosting considerations

If the user runs their own MTA (Postfix, mailcow, Mailu, Stalwart, Maddy, Mail-in-a-Box, iRedMail,
Mox), the DNS set is larger and the non-DNS requirements decide deliverability:

- `mail.example.com` A and AAAA, and matching **PTR** records on both addresses set at the hosting
  provider (not in the domain's zone). Missing or mismatched reverse DNS is the single biggest
  cause of rejection from Microsoft and Gmail for self-hosters.
- Static IP with clean history; residential and many cheap VPS ranges are blocklisted wholesale.
  Check Spamhaus, Barracuda, Microsoft SNDS before committing. Port 25 outbound must be open.
- SPF for the root (`v=spf1 mx -all` or `a:mail.example.com -all`) and for the HELO name.
- DKIM TXT (2048-bit) generated on the server; two selectors for rotation.
- DMARC as usual; MTA-STS and TLS-RPT are easy and worth doing; DANE (TLSA at `_25._tcp.mail`)
  only if the DNS host supports DNSSEC and the user will maintain certificate rotation hooks.
- `autoconfig`/`autodiscover`/SRV records pointing at the server.
- Consider sending through a relay (SES, Postmark, Mailgun) even when receiving locally; many
  self-hosters land on this after fighting IP reputation.

## Account-level security

Not DNS, but every mail DNS conversation should surface it because the domain *is* the identity:

- Registrar: 2FA, auto-renew with a valid payment method, registrar lock / transfer lock, and a
  contact email that is **not** on the domain itself (a lost domain must not take its own recovery
  address down with it).
- DNS host: 2FA; audit API tokens; scope automation tokens to the zones they need.
- Mailbox provider: 2FA, per-device app passwords, review of forwarding rules (attackers add silent
  forwards), and provider features like "account reset via DNS" enabled on one hardened domain only.
- Keep a written list of every service authorized to send as each domain; review it when reading
  DMARC reports.

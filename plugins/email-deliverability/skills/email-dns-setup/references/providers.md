# Provider record templates

Contents: [How to use this file](#how-to-use-this-file) · [Mailbox providers](#mailbox-providers) ·
[Transactional senders](#transactional-senders) · [Marketing platforms](#marketing-platforms) ·
[Helpdesk / CRM](#helpdesk-and-crm-tools) · [Self-hosted servers](#self-hosted-servers) ·
[Unknown provider](#any-provider-not-listed)

## How to use this file

These templates capture the *shape* of each provider's records and the selectors they use as of
late 2026. Providers change MX hosts, add selectors and move documentation. Treat every value here
as "confirm against the provider's current docs or the user's admin portal", and say so in the
output. Per-domain values (ownership tokens, per-domain DKIM CNAME targets, per-account SES
selectors) are only available from the portal; mark them `<from portal>`.

Two things are always the user's own, regardless of provider: the DMARC record (own it, start at
`p=none` with `rua=`; see records.md) and the decision about which subdomain each sender lives on
(architecture.md).

## Mailbox providers

### Google Workspace

```
@                 MX    1   smtp.google.com.                     ; single MX since 2023; legacy 5-host set still works
@                 TXT       "v=spf1 include:_spf.google.com ~all"
google._domainkey TXT       "v=DKIM1; k=rsa; p=<2048-bit key from Admin console > Apps > Gmail > Authenticate email>"
@                 TXT       "google-site-verification=<token>"   ; if not verified via another method
_dmarc            TXT       "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
```

Notes: DKIM is off until "Start authentication" is clicked in the Admin console; the key is a TXT
(not CNAME), 2048-bit, so split at 255 chars. Selector is `google` by default but can be custom.
Docs: Google Workspace Admin Help → "Set up MX records", "Turn on DKIM".

### Microsoft 365 / Exchange Online

```
@                        MX    0   <tenant>-com.mail.protection.outlook.com.   ; from admin center
@                        TXT       "v=spf1 include:spf.protection.outlook.com -all"
selector1._domainkey     CNAME     selector1-<tenant>-com._domainkey.<tenant>.onmicrosoft.com.
selector2._domainkey     CNAME     selector2-<tenant>-com._domainkey.<tenant>.onmicrosoft.com.
autodiscover             CNAME     autodiscover.outlook.com.
@                        TXT       "MS=ms<digits>"                ; ownership, can be removed after verification
_dmarc                   TXT       "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
```

Notes: DKIM must be enabled per domain in the Defender portal after the CNAMEs exist. Tenant
names with hyphens or non-.com TLDs change the CNAME target; copy from the portal. Teams/Intune
records (`enterpriseregistration`, `enterpriseenrollment`, `sip`, `lyncdiscover`, `_sip._tls`,
`_sipfederationtls._tcp`) only if those services are used. Docs: learn.microsoft.com → "Add DNS
records to connect your domain".

### Fastmail

```
@                  MX    10  in1-smtp.messagingengine.com.
@                  MX    20  in2-smtp.messagingengine.com.
@                  TXT       "v=spf1 include:spf.messagingengine.com ?all"   ; Fastmail suggests ?all; -all is fine once DMARC confirms
fm1._domainkey     CNAME     fm1.example.com.dkim.fmhosted.com.
fm2._domainkey     CNAME     fm2.example.com.dkim.fmhosted.com.
fm3._domainkey     CNAME     fm3.example.com.dkim.fmhosted.com.
_dmarc             TXT       "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
; optional client config:
_submission._tcp   SRV   0 1 587 smtp.fastmail.com.
_imaps._tcp        SRV   0 1 993 imap.fastmail.com.
_caldavs._tcp      SRV   0 1 443 caldav.fastmail.com.
_carddavs._tcp     SRV   0 1 443 carddav.fastmail.com.
autoconfig         CNAME     autoconfig.fastmail.com.
```

Notes: DKIM CNAME targets embed the user's domain. Fastmail can also host the domain's DNS
entirely (then everything is automatic). Docs: fastmail.help → "Manual DNS configuration".

### Proton Mail

```
@                       MX    10  mail.protonmail.ch.
@                       MX    20  mailsec.protonmail.ch.
@                       TXT       "v=spf1 include:_spf.protonmail.ch ~all"
protonmail._domainkey   CNAME     protonmail.domainkey.<id>.domains.proton.ch.
protonmail2._domainkey  CNAME     protonmail2.domainkey.<id>.domains.proton.ch.
protonmail3._domainkey  CNAME     protonmail3.domainkey.<id>.domains.proton.ch.
@                       TXT       "protonmail-verification=<token>"
_dmarc                  TXT       "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
```

Notes: all three selectors are required. Docs: proton.me/support → "Custom domain".

### iCloud Mail (Custom Email Domain)

```
@                 MX    10  mx01.mail.icloud.com.
@                 MX    10  mx02.mail.icloud.com.
@                 TXT       "v=spf1 include:icloud.com ~all"
sig1._domainkey   CNAME     sig1.dkim.example.com.at.icloudmailadmin.com.
@                 TXT       "apple-domain=<token>"
_dmarc            TXT       "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
```

Docs: support.apple.com → "Set up an existing domain with iCloud Mail".

### Zoho Mail

```
@                MX    10  mx.zoho.com.        ; .eu / .in / .com.au variants per data center
@                MX    20  mx2.zoho.com.
@                MX    50  mx3.zoho.com.
@                TXT       "v=spf1 include:zohomail.com ~all"    ; region-specific include per portal
zmail._domainkey TXT       "v=DKIM1; k=rsa; p=<from Zoho admin>"  ; selector chosen by admin
@                TXT       "zoho-verification=<token>"
_dmarc           TXT       "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
```

### Purelymail

```
@                        MX    50  mailserver.purelymail.com.
@                        TXT       "v=spf1 include:_spf.purelymail.com ~all"
@                        TXT       "purelymail_ownership_proof=<from portal>"
purelymail1._domainkey   CNAME     key1.dkimroot.purelymail.com.
purelymail2._domainkey   CNAME     key2.dkimroot.purelymail.com.
purelymail3._domainkey   CNAME     key3.dkimroot.purelymail.com.
_dmarc                   TXT       "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
```

Notes: Purelymail suggests a `_dmarc` CNAME to its own record, which is `p=reject` with only a
`ruf=` to Purelymail. Decline it and publish the TXT above; the portal checker will say "not
recognized", which Purelymail staff confirm is fine. Routing rules handle `postmaster@`, `abuse@`,
role aliases and subaddressing (`user+tag@`). Aliases can use webmail but not IMAP. Docs:
purelymail.com/docs/domainDocs.

### Migadu

```
@                  MX    10  aspmx1.migadu.com.
@                  MX    20  aspmx2.migadu.com.
@                  TXT       "v=spf1 include:spf.migadu.com -all"
key1._domainkey    CNAME     key1.example.com._domainkey.migadu.com.
key2._domainkey    CNAME     key2.example.com._domainkey.migadu.com.
key3._domainkey    CNAME     key3.example.com._domainkey.migadu.com.
@                  TXT       "hosted-email-verify=<token>"
_dmarc             TXT       "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
autoconfig         CNAME     autoconfig.migadu.com.
_autodiscover._tcp SRV   0 1 443 autodiscover.migadu.com.
_submissions._tcp  SRV   0 1 465 smtp.migadu.com.
_imaps._tcp        SRV   0 1 993 imap.migadu.com.
```

### mailbox.org, Posteo, Tuta, Hey, Runbox, Mailfence, Namecheap Private Email, Hostinger, cPanel hosts

Same shape: MX set, one SPF include, one to three DKIM selectors (usually CNAME), verification
TXT, own DMARC. Pull exact values from the provider; do not guess selectors. cPanel/Plesk hosts
generate a per-domain `default._domainkey` TXT in the panel and need the server's IP (or `+a +mx`)
in SPF.

## Transactional senders

Set these on a **sending subdomain** (`notify.example.com`) unless the user explicitly needs
`d=example.com`. Each service also issues a *return-path* / bounce CNAME so SPF aligns; set it.

### Postmark

```
<timestamp>pm._domainkey.notify  TXT  "k=rsa; p=<from Postmark>"    ; hostname like 20261016pm._domainkey; TXT, not CNAME
pm-bounces.notify           CNAME  pm.mtasv.net.                      ; custom return-path
```

SPF not required (Postmark return-path is on pm.mtasv.net until the CNAME above, then aligned).
Postmark's free DMARC digest service is a good `rua=` target.

### Amazon SES

```
<sel1>._domainkey.notify    CNAME  <sel1>.dkim.amazonses.com.         ; Easy DKIM issues 3 selectors
<sel2>._domainkey.notify    CNAME  <sel2>.dkim.amazonses.com.
<sel3>._domainkey.notify    CNAME  <sel3>.dkim.amazonses.com.
bounce.notify               MX     10 feedback-smtp.<region>.amazonses.com.   ; custom MAIL FROM
bounce.notify               TXT    "v=spf1 include:amazonses.com ~all"
```

Notes: MX hostname is region-specific. Without the custom MAIL FROM, SPF never aligns (only DKIM
does), which is acceptable but weaker. Sandbox accounts must request production access.

### Resend

```
resend._domainkey.notify    TXT    "p=<from Resend>"
send.notify                 MX     10 feedback-smtp.<region>.amazonses.com.   ; Resend runs on SES
send.notify                 TXT    "v=spf1 include:amazonses.com ~all"
```

### SendGrid

```
em<digits>.notify           CNAME  u<id>.wl<id>.sendgrid.net.       ; link branding / return-path
s1._domainkey.notify        CNAME  s1.domainkey.u<id>.wl<id>.sendgrid.net.
s2._domainkey.notify        CNAME  s2.domainkey.u<id>.wl<id>.sendgrid.net.
```

### Mailgun

```
notify                      TXT    "v=spf1 include:mailgun.org ~all"
<sel>._domainkey.notify     TXT    "k=rsa; p=<from Mailgun>"
email.notify                CNAME  mailgun.org.                      ; tracking
notify                      MX     10 mxa.mailgun.org.               ; only if receiving on the subdomain
notify                      MX     10 mxb.mailgun.org.
```

EU region uses `mailgun.org` includes too but different MX hosts; check the control panel.

### Brevo (Sendinblue), Mailjet, SparkPost, Postal, Loops, Customer.io transactional, Mailtrap

Same shape: one or two DKIM records (CNAME or TXT), an SPF include or a return-path CNAME,
sometimes a verification TXT. Copy from the dashboard.

## Marketing platforms

Set on a marketing subdomain (`news.example.com`). All of these now require authenticated sending
domains because of Gmail/Yahoo bulk-sender rules (DKIM alignment, one-click unsubscribe, complaint
rate < 0.3%).

- **Mailchimp**: `k2._domainkey.news CNAME dkim2.mcsv.net.`, `k3._domainkey.news CNAME dkim3.mcsv.net.`,
  `_dmarc` on the subdomain or inherit via org `sp=`. Mailchimp no longer needs an SPF include.
- **Kit (ConvertKit)**: two DKIM CNAMEs and a return-path CNAME issued per account.
- **Beehiiv**: three CNAMEs (two DKIM, one return-path) per publication.
- **Klaviyo**: `kl._domainkey` and `kl2._domainkey` CNAMEs plus a `send.`/`ksd.` return-path CNAME.
- **Customer.io, HubSpot, ActiveCampaign, Buttondown, Substack custom domain, Drip, Constant Contact**:
  dashboard-issued CNAMEs; same pattern.

Ask whether the From address will be on the subdomain (`hello@news.example.com`) or the root
(`hello@example.com`). Root From with subdomain DKIM works under relaxed alignment but then the
root's reputation is still partly at stake; most receivers key on the `d=` and the From domain.

## Helpdesk and CRM tools

Zendesk, Front, Help Scout, Intercom, HubSpot Sales, Freshdesk, Gorgias, Missive and similar send
*as the root domain* on behalf of staff. They need DKIM selectors on the root (CNAMEs issued per
tool) and sometimes an SPF include on the root. Add each to the running count of SPF lookups and
to the written list of authorized senders. Many also want the root's MX to forward a support
address to them; prefer a provider-side routing rule over changing MX.

## Self-hosted servers

mailcow, Mailu, Stalwart, Maddy, Mail-in-a-Box, iRedMail, Mox, Postfix+Dovecot by hand. DNS the
server needs (plus the operational items in architecture.md):

```
mail                A      <ipv4>
mail                AAAA   <ipv6>
@                   MX     10 mail.example.com.
@                   TXT    "v=spf1 mx -all"
mail                TXT    "v=spf1 a -all"                 ; HELO identity
dkim._domainkey     TXT    "v=DKIM1; k=rsa; p=<2048-bit, split at 255>"   ; selector chosen on server
_dmarc              TXT    "v=DMARC1; p=none; rua=mailto:dmarc@example.com"
_mta-sts            TXT    "v=STSv1; id=<timestamp>"
mta-sts             A/CNAME -> host serving /.well-known/mta-sts.txt
_smtp._tls          TXT    "v=TLSRPTv1; rua=mailto:tls-reports@example.com"
autoconfig          CNAME  mail.example.com.
autodiscover        CNAME  mail.example.com.
_imaps._tcp         SRV    0 1 993 mail.example.com.
_submissions._tcp   SRV    0 1 465 mail.example.com.
_submission._tcp    SRV    0 1 587 mail.example.com.
_25._tcp.mail       TLSA   3 1 1 <sha256 of cert SPKI>        ; DANE, only with DNSSEC
```

PTR records for both addresses are set at the VPS/hosting provider, not in this zone. Mailcow,
Mail-in-a-Box, Mox and Stalwart print the exact record set they expect; use that as the source
of truth and verify with the audit script.

## Any provider not listed

1. Open the provider's "custom domain" / "DNS records" doc or the admin portal page that lists
   records; copy values verbatim into the table template.
2. Identify which records are *identity* (MX, verification token), *authentication* (SPF include,
   DKIM selectors) and *convenience* (autodiscover, SRV, tracking CNAMEs). All identity and
   authentication records are mandatory; convenience ones are optional.
3. Replace any provider-supplied DMARC suggestion with the user's own `p=none; rua=` record.
4. Note whether the DKIM record is CNAME or TXT and whether the key exceeds 255 characters.
5. Count SPF lookups for the include they give (`scripts/check_mail_dns.sh` does this for a
   published record; `dig TXT _spf.provider.example` to pre-check an include).

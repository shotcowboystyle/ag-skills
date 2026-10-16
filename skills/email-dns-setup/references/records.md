# Mail DNS record reference

Contents: [MX](#mx) · [SPF](#spf) · [DKIM](#dkim) · [DMARC](#dmarc) · [MTA-STS](#mta-sts) ·
[TLS-RPT](#tls-rpt) · [BIMI](#bimi) · [Autodiscover / SRV](#client-autoconfiguration) ·
[Null MX lockdown](#locking-down-a-domain-that-never-sends) · [TXT syntax rules](#txt-syntax-rules) ·
[Verification commands](#verification-commands)

All examples use `example.com`. Hosts are written relative to the zone (`@` = apex). Trailing dots on
target hostnames are correct in zone files and most APIs; many web UIs add them automatically.

## MX

Where inbound mail is delivered. Lower priority number wins; equal numbers are load-balanced.

```
@   MX  10  mx1.provider.example.
@   MX  20  mx2.provider.example.
```

Rules:
- Target must be a hostname with an A/AAAA record, never an IP and never a CNAME (RFC 2181 §10.3).
  Many receivers tolerate a CNAME target but some reject it; providers publish real hostnames.
- One provider's MX set only. Mixing two providers' MX records splits inbound mail unpredictably.
- Subdomains that only *send* (transactional, marketing) still benefit from an MX so bounces and
  replies have somewhere to go; most sending services provide one (`feedback-smtp.*`, `inbound.*`).
- Delete old MX before or at the same moment as adding the new; a long overlap means mail lands in
  the old mailbox for some senders.

## SPF

A TXT record at the sending name listing which servers may use that name in the SMTP envelope
sender (MAIL FROM / Return-Path). Receivers check the envelope domain, which for transactional
services is usually *their* bounce domain unless a custom return-path is configured; that is why
DKIM alignment matters more than SPF for most third-party senders. Still publish SPF everywhere.

```
@   TXT  "v=spf1 include:_spf.provider.example include:_spf.other.example -all"
```

Syntax:
- Must start with `v=spf1`. Exactly one SPF TXT record per name; two is a `permerror` (treated as
  no SPF at all). Merge includes into one record. The old `SPF` RRtype is obsolete; use TXT.
- Mechanisms: `include:` (another domain's policy), `a`, `mx`, `ip4:`, `ip6:`, `exists:`,
  `redirect=`. `ptr` is deprecated; remove it if seen.
- Qualifiers: `-all` fail, `~all` softfail, `?all` neutral, `+all` pass everything (never use).
  Choose `-all` for people mail and locked-down domains; `~all` is acceptable while migrating.
- **10-lookup limit**: `include`, `a`, `mx`, `ptr`, `exists`, `redirect` each cost one DNS lookup,
  recursively through every include. Over 10 is `permerror`. Some providers' includes nest several levels deep; count them, never assume.
  The audit script counts them. Fixes, in order of preference: move senders to subdomains with
  their own SPF; replace `include` with `ip4:` ranges only when the provider documents them as
  stable; use a flattening service as a last resort (it must re-flatten automatically).
- Void lookups (names that return NXDOMAIN) are limited to 2.
- Length: one TXT record, but strings inside it may be split at 255 characters (see TXT syntax).
- SPF on a subdomain is independent; `notify.example.com` needs its own record. A subdomain with no
  SPF record has no SPF policy (it does not inherit).
- The `HELO`/`EHLO` hostname of a self-hosted server also gets checked; give `mail.example.com`
  its own `v=spf1 a -all`.

## DKIM

A public key at `<selector>._domainkey.<domain>`; the provider signs outgoing mail with the
matching private key. Receivers verify the signature and check that the `d=` domain aligns with
the From header domain for DMARC.

Two publication styles:

1. **CNAME to the provider** (preferred when offered; provider rotates keys without DNS changes):
   ```
   selector1._domainkey   CNAME  selector1.dkim.provider.example.
   ```
   Must not be proxied/flattened by the DNS host. The target hostname resolves to a TXT record,
   so a host that only "flattens" to A/AAAA breaks it.

2. **TXT with the key** (self-hosted, and some providers):
   ```
   sel2024._domainkey   TXT  "v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA..."
   ```
   2048-bit keys exceed 255 characters: publish as multiple quoted strings inside one record
   (`"v=DKIM1; k=rsa; p=MIIB..." "...rest..."`). Receivers concatenate them. Some host UIs do
   this automatically, others need the quotes typed in, and a few (notably older GoDaddy and
   some registrars' free DNS) cannot store it at all; use a 1024-bit key only as a last resort
   and rotate it more often, or move DNS.
   Optional tags: `t=s` (strict, no subdomain use), `t=y` (testing, treat failures as pass; remove
   in production), `h=sha256`.

Rules:
- Selector names are provider-specific (`google`, `selector1`/`selector2`, `fm1`/`fm2`/`fm3`,
  `protonmail`/`protonmail2`/`protonmail3`, `purelymail1..3`, `pm`, `resend`, `s1`/`s2`,
  `k1`...). Never guess a selector; take it from the provider's docs or portal.
- Publish **all** selectors a provider lists. Providers rotate between them; a missing one means
  intermittent failures that are very hard to diagnose.
- Delete selectors of providers no longer used. An old provider that can still sign as the domain
  is a liability.
- Ed25519 keys (`k=ed25519`) are valid but not universally verified yet; publish alongside RSA
  (dual-signing) rather than instead of it.
- Key rotation: at least yearly for self-managed keys; publish the new selector, switch signing,
  wait a week, remove the old one.

## DMARC

TXT at `_dmarc.<domain>`. Tells receivers what to do when neither SPF nor DKIM passes **in
alignment** with the From-header domain, and where to send reports.

```
_dmarc   TXT  "v=DMARC1; p=none; rua=mailto:dmarc@example.com; ruf=mailto:dmarc@example.com; fo=1; adkim=r; aspf=r; pct=100"
```

Tags:
- `p=` policy for the domain: `none` (monitor), `quarantine` (spam folder), `reject`.
- `sp=` policy for subdomains without their own `_dmarc`. Defaults to `p`. For a domain whose
  subdomains all have explicit records, `sp=reject` closes off every other subdomain.
- `rua=` aggregate (daily XML summaries). The useful one. Always include it.
- `ruf=` forensic/failure samples. Few receivers send them (Gmail does not); harmless to include.
- `fo=1` request a failure report when either SPF or DKIM fails (default `0` requires both).
- `adkim=`/`aspf=`: `r` relaxed (subdomain of the From domain counts as aligned) or `s` strict.
  Relaxed is correct when transactional mail goes out from subdomains; strict is for domains
  where everything is sent exactly from the apex.
- `pct=` percentage of failing mail the policy applies to. Useful for a staged move to
  `quarantine` (`pct=25`, `50`, `100`). Do not leave a non-100 value in place long-term.
- Reports to a different domain: the receiving domain must publish
  `example.com._report._dmarc.reports.example.net TXT "v=DMARC1"` or reports are not sent.
  Hosted DMARC services set this up on their side; Cloudflare DMARC Management does it
  automatically when enabled.

Rollout (state this plan in every setup; it is the part users skip):

| Phase | Record | Exit criterion |
|---|---|---|
| 1 | `p=none; rua=...` | 2 to 4 weeks of reports; every legitimate source passes DKIM or SPF in alignment |
| 2 | `p=quarantine; pct=25` then `pct=100` | one to two weeks with no legitimate mail quarantined |
| 3 | `p=reject` | done; keep reading reports monthly |

Do not CNAME `_dmarc` to a provider's record (e.g. a provider that publishes `p=reject` with
its own `ruf`): it starts at enforcement with no aggregate reports to the user, so forgotten
senders are dropped with no visibility. Own the record. If the provider's setup checker then
complains that the DMARC record is "not recognized", that is expected.

Reading reports: raw XML is not meant for humans. Point `rua=` at Cloudflare DMARC Management,
Postmark's DMARC digest, dmarcian, Valimail, EasyDMARC, or Fastmail's/Google's built-in views,
depending on what the user already has.

## MTA-STS

Tells sending servers to require TLS with a valid certificate when delivering to the domain's MX.
Two parts: a DNS TXT record that versions the policy, and an HTTPS-served policy file.

```
_mta-sts   TXT  "v=STSv1; id=20261016T120000"
```

Policy file at `https://mta-sts.example.com/.well-known/mta-sts.txt`, served with a valid
certificate for `mta-sts.example.com`:

```
version: STSv1
mode: testing
mx: mx1.provider.example
mx: mx2.provider.example
max_age: 604800
```

- `mode: testing` first, then `enforce` after TLS-RPT shows no failures. `mx:` lines must match
  the actual MX hostnames (wildcards like `*.provider.example` are allowed).
- Change `id=` every time the policy file changes; senders cache by it.
- Hosting the file: Cloudflare Pages/Workers, GitHub Pages, Vercel, an S3+CloudFront bucket, or any
  static host; some mailbox providers (Fastmail, Proton, Google) host it or document a CNAME.
- Skip MTA-STS for a domain whose MX provider does not publish a stable MX list.

## TLS-RPT

Daily reports about TLS negotiation failures to the domain's MX. Pairs with MTA-STS.

```
_smtp._tls   TXT  "v=TLSRPTv1; rua=mailto:tls-reports@example.com"
```

## BIMI

Brand logo next to messages in supporting clients. Requirements before it does anything:
DMARC at `p=quarantine` (pct=100) or `p=reject` on the domain, an SVG Tiny PS logo on HTTPS, and
for Gmail/Apple a Verified Mark Certificate (paid, needs a registered trademark) or Common Mark
Certificate.

```
default._bimi   TXT  "v=BIMI1; l=https://example.com/brand/logo.svg; a=https://example.com/brand/vmc.pem"
```

Mention it as optional; do not recommend it for small domains unless they ask.

## Client autoconfiguration

Helps mail clients find IMAP/SMTP settings from the address alone. Only relevant for mailbox
providers (not sending subdomains). Providers document their exact set; the common ones:

```
autoconfig      CNAME  autoconfig.provider.example.      ; Thunderbird
autodiscover    CNAME  autodiscover.provider.example.    ; Outlook (Microsoft 365: autodiscover.outlook.com)
_imaps._tcp     SRV    0 1 993 imap.provider.example.    ; RFC 6186
_submission._tcp SRV   0 1 587 smtp.provider.example.
_pop3s._tcp     SRV    0 0 0 .                           ; explicitly "no POP"
_caldavs._tcp / _carddavs._tcp  SRV ...                  ; calendar/contacts if offered
```

Microsoft 365 additionally uses `enterpriseregistration` and `enterpriseenrollment` CNAMEs for
device management, and historically `lyncdiscover`/`sip` for Teams; include only what the
provider's admin center lists for the tenant.

## Locking down a domain that never sends

Parked domains, redirect-only brand domains, and businesses with no email are the easiest
phishing targets because nothing says "no mail comes from here". Publish all four:

```
@             MX   0   .                      ; null MX, RFC 7505: "this domain accepts no mail"
@             TXT      "v=spf1 -all"          ; no server may send as this domain
_dmarc        TXT      "v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s;"
*._domainkey  TXT      "v=DKIM1; p="          ; every DKIM selector is revoked
```

Some host UIs refuse a `.` MX target; enter the record through the API or accept the host's
"null MX" preset if it has one. Optionally add `rua=` so the owner sees attempted abuse.

Subdomains of a mail-enabled domain that never send (`www`, `api`, `cdn`) are covered by the
parent's `sp=reject` once that is set; no per-subdomain records are needed.

## TXT syntax rules

- Each quoted string is at most 255 characters; a record may contain several strings, which
  receivers concatenate with no separator. Split long DKIM keys or SPF at any point, never inside
  a tag name.
- Zone-file quoting (`"v=spf1 ... -all"`) is what `dig` shows. Web UIs usually want the value
  without the outer quotes. The Route 53 console and raw API require them; Terraform/OpenTofu
  providers (AWS, Cloudflare) add them for you, so never quote inside the HCL string. Check with
  `dig` after entry; a value shown as `"\"v=spf1 ...\""` has doubled quotes and will not validate.
- Case: tags are case-insensitive, but DKIM `p=` and selectors must be copied exactly.
- Semicolons: DMARC and DKIM use `;` separators with optional spaces; SPF uses spaces only.
- Some UIs silently strip a trailing `;` or add a space; harmless for DMARC, fatal inside a DKIM key.

## Verification commands

```bash
dig +short NS example.com                       # who actually serves the zone
dig +short MX example.com
dig +short TXT example.com | grep spf1          # exactly one line
dig +short TXT selector._domainkey.example.com  # or CNAME
dig +short TXT _dmarc.example.com
dig +short TXT _mta-sts.example.com; curl -s https://mta-sts.example.com/.well-known/mta-sts.txt
dig +short TXT _smtp._tls.example.com
dig @ns1.authoritative.example TXT _dmarc.example.com   # bypass caches right after a change
```

Then send a real message to Gmail and read "Show original": `SPF: PASS with IP ...`,
`DKIM: 'PASS' with domain example.com`, `DMARC: 'PASS'`. A DKIM domain that is the provider's
(`d=provider.example`) means the user's selectors are not resolving; recheck for proxying,
zone auto-append, or a typo in the selector.

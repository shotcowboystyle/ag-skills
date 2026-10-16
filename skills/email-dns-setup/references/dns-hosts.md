# DNS host and registrar specifics

Contents: [First: identify the real DNS host](#identify-the-real-dns-host) · [Cloudflare](#cloudflare) ·
[Route 53](#amazon-route-53) · [Namecheap](#namecheap) · [GoDaddy](#godaddy) · [Porkbun](#porkbun) ·
[Vercel DNS](#vercel-dns) · [Squarespace (ex Google Domains)](#squarespace-domains-ex-google-domains) ·
[DigitalOcean / Linode / Hetzner / Vultr](#digitalocean-linode-hetzner-vultr) · [Google Cloud DNS / Azure DNS](#google-cloud-dns-and-azure-dns) ·
[Hover, Gandi, OVH, IONOS, Bluehost, Hostinger, cPanel](#other-common-hosts) · [Infrastructure as code](#infrastructure-as-code) ·
[external-dns and Kubernetes](#external-dns-and-kubernetes) · [Generic entry rules](#generic-entry-rules-for-any-ui)

## Identify the real DNS host

The registrar is where the domain is paid for; the DNS host is whoever the NS records point at.
They often differ (domain at Namecheap, DNS at Cloudflare; domain at GoDaddy, DNS at Route 53).
Always run:

```bash
dig +short NS example.com
```

and map the result: `*.ns.cloudflare.com` → Cloudflare, `ns-*.awsdns-*` → Route 53,
`dns1.registrar-servers.com` → Namecheap BasicDNS, `ns*.domaincontrol.com` → GoDaddy,
`*.porkbun.com` → Porkbun, `ns1.vercel-dns.com` → Vercel, `ns-cloud-*.googledomains.com` →
Google Cloud DNS/Squarespace, `ns*.digitalocean.com` → DigitalOcean, `*.ns.hetzner.*` → Hetzner.
Records entered anywhere other than the NS host do nothing.

## Cloudflare

- **Proxy status**: every mail-related CNAME (DKIM, autodiscover, return-path, tracking) and any
  `mail.`/`mx.` A record must be **DNS only** (grey cloud). Proxied CNAMEs resolve to Cloudflare
  IPs and DKIM lookups return nothing. MX and TXT cannot be proxied, but their *targets* can be;
  check the `mail` A record if it exists.
- Apex entry: use `@` or the bare domain; Cloudflare displays the full name.
- TXT values: enter without outer quotes; Cloudflare splits >255-char values automatically.
- Null MX: Cloudflare accepts `.` as the MX target in the UI and API.
- Cloudflare **DMARC Management** (Email → DMARC Management) creates the `rua=` endpoint and
  parses reports; good default for `rua=` when the zone is on Cloudflare.
- Cloudflare **Email Routing** (forwarding to another mailbox) takes over MX and SPF for the zone;
  it cannot coexist with another provider's MX. Disable it before pointing MX at a mailbox provider.
- Cloudflare **Email Security DNS Wizard** offers to add lockdown records for domains without mail;
  the manual set in records.md is equivalent.
- API example:
  ```bash
  curl -sX POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
    -H "Authorization: Bearer $CF_API_TOKEN" -H "Content-Type: application/json" \
    --data '{"type":"CNAME","name":"fm1._domainkey","content":"fm1.example.com.dkim.fmhosted.com","proxied":false,"ttl":3600}'
  ```
- OpenTofu/Terraform: `cloudflare_dns_record` (provider v5; `cloudflare_record` in v4) with
  `proxied = false`. Snippet in the IaC section.

## Amazon Route 53

- Apex: enter the full name `example.com` (the console pre-fills it); subdomains as `_dmarc.example.com`.
- TXT values **must be wrapped in double quotes** in the console and API, one quoted string per
  line for multiple strings; >255-char DKIM keys as `"part1" "part2"` on one line.
- Multiple MX in one record set: one line per `priority host` pair.
- Null MX: value `0 .` works.
- CLI: `aws route53 change-resource-record-sets --hosted-zone-id Z... --change-batch file://mail.json`.
- Terraform/OpenTofu: `aws_route53_record` with `records = ["v=spf1 include:... -all"]`, **no
  inner quotes**. The AWS provider wraps each TXT value in quotes itself; adding your own produces
  `""v=spf1...""` and a rejected or broken record. To split a >255-char DKIM key, put `\"\"` at the
  split point inside one string (`"first255chars\"\"rest"`), which the provider turns into two
  quoted strings. Console and raw API calls are the opposite: there the value must be quoted.
- Alias records exist only for AWS targets; irrelevant for mail.
- Route 53 health-checked / weighted record sets must not be used for MX.

## Namecheap

- Registrar and often DNS host (BasicDNS / PremiumDNS). If nameservers were changed to Cloudflare
  or another host, Namecheap's "Advanced DNS" tab does nothing.
- Apex: `@`. Subdomains: relative (`_dmarc`, `fm1._domainkey`).
- "Mail Settings" dropdown on the Advanced DNS tab must be set to **Custom MX** before MX records
  can be entered; the "Private Email" or "Email Forwarding" presets overwrite MX and SPF.
- TXT: no quotes; long DKIM keys are accepted.
- Null MX: some accounts reject `.`; use the API or enter `0 .` and verify with `dig`.
- Email forwarding (free) sets its own MX (`eforward*.registrar-servers.com`); turn it off before
  using a mailbox provider.

## GoDaddy

- Apex: `@`. GoDaddy UI used to append the domain automatically and reject names containing the
  domain; enter relative names only.
- TXT: no quotes; legacy UI truncated values over 255 chars (breaks 2048-bit DKIM TXT). Current
  UI accepts them, but verify with `dig`; if it fails, use the provider's CNAME form or move DNS.
- Microsoft 365 and Google Workspace have "connect" wizards that write records automatically and
  sometimes leave stale duplicates; audit afterwards.
- Workspace Email / Office 365 from GoDaddy adds its own MX/SPF; remove them if switching providers.

## Porkbun

- Apex: leave the host field blank. Subdomains: relative.
- TXT: no quotes. Null MX: accepted via UI (`.`) and API.
- Free email forwarding adds `fwd1/fwd2.porkbun.com` MX; disable it before setting provider MX.
- API: `POST https://api.porkbun.com/api/json/v3/dns/create/example.com` with
  `{"type":"TXT","name":"_dmarc","content":"v=DMARC1; p=none; rua=mailto:...","ttl":"600"}`.

## Vercel DNS

- Only active when the domain's nameservers are `ns1/ns2.vercel-dns.com`. A domain merely
  *added to a Vercel project* (A/CNAME at another host) is not using Vercel DNS.
- Apex: leave name blank or `@`. TXT without quotes; MX with priority field.
- Vercel-bought domains default to Vercel DNS; CLI: `vercel dns add example.com _dmarc TXT "v=DMARC1; p=none; rua=mailto:dmarc@example.com"`,
  `vercel dns add example.com @ MX mx1.provider.example 10`.
- Dashboard shows a warning banner for missing SPF/DMARC on some plans; it is advisory.

## Squarespace Domains (ex Google Domains)

- Domains migrated from Google Domains keep working; DNS editor at account.squarespace.com.
- Apex: `@`. TXT: no quotes. Google Workspace records can be auto-added from the Workspace panel.
- Squarespace "email forwarding" and "Google Workspace via Squarespace" both manage MX; disable
  before pointing MX elsewhere.
- Google Cloud DNS nameservers (`ns-cloud-*.googledomains.com`) may still appear on some zones;
  the editor is still Squarespace's.

## DigitalOcean, Linode, Hetzner, Vultr

- These are usually the DNS host for self-hosted mail. Apex: `@`. TXT: no quotes.
- **PTR records** live under the Droplet/Server/Instance network settings, not the zone: set the
  reverse name to `mail.example.com` on both IPv4 and IPv6. DigitalOcean derives PTR from the
  Droplet *name*; rename the Droplet to `mail.example.com`.
- Hetzner DNS console accepts zone-file import, which is the fastest way to add a full mail set.
- Outbound port 25 is blocked by default on new Hetzner, Vultr, DigitalOcean and Linode accounts;
  it must be requested.

## Google Cloud DNS and Azure DNS

- Cloud DNS: record sets, TXT data quoted; `gcloud dns record-sets create _dmarc.example.com. --zone=... --type=TXT --ttl=3600 --rrdatas='"v=DMARC1; p=none; rua=mailto:dmarc@example.com"'`.
- Azure DNS: apex is `@`; TXT values may be split automatically; `az network dns record-set txt add-record ...`.
- Both are frequently managed by Terraform; prefer editing the code over the console.

## Other common hosts

- **Hover**: apex `@`, TXT no quotes; email forwarding sets MX, disable first.
- **Gandi**: LiveDNS, zone-file editor available; apex `@`; Gandi Mail adds MX/SPF if enabled.
- **OVH**: apex blank; "MX Plan" and "Exchange" offers manage MX; TXT in quotes in the zone view.
- **IONOS**: apex `@`; "Email & Office" products lock MX until the product is removed.
- **Bluehost / HostGator / SiteGround / cPanel Zone Editor**: records belong to the hosting account;
  cPanel auto-creates `mail.`, `webmail.`, `default._domainkey` and an SPF with `+a +mx +ip4`; replace
  them when moving mail off the host. "Email Routing" in cPanel must be set to *Remote Mail
  Exchanger* or the server keeps delivering locally even with external MX.
- **Hostinger**: hPanel DNS zone; its own email product sets MX; disable to use another provider.
- **Wix / Squarespace sites / Shopify / Webflow hosting DNS**: pointing nameservers at a site
  builder means editing mail records in that builder's limited DNS panel; most support MX/TXT/CNAME
  but not SRV or null MX. If mail needs more, move DNS to a real host and point the site with A/CNAME.

## Infrastructure as code

If the user already manages the zone with OpenTofu/Terraform, Pulumi, octoDNS or dnscontrol,
write the records there. Keep mail records in their own file/module so they are reviewable.

OpenTofu + Cloudflare provider v5:
```hcl
locals {
  zone_id = "..."
  dkim = { fm1 = "fm1.example.com.dkim.fmhosted.com", fm2 = "fm2.example.com.dkim.fmhosted.com", fm3 = "fm3.example.com.dkim.fmhosted.com" }
}

resource "cloudflare_dns_record" "mx" {
  for_each = { "in1-smtp.messagingengine.com" = 10, "in2-smtp.messagingengine.com" = 20 }
  zone_id  = local.zone_id
  name     = "example.com"
  type     = "MX"
  content  = each.key
  priority = each.value
  ttl      = 3600
}

resource "cloudflare_dns_record" "spf" {
  zone_id = local.zone_id
  name    = "example.com"
  type    = "TXT"
  content = "\"v=spf1 include:spf.messagingengine.com -all\""
  ttl     = 3600
}

resource "cloudflare_dns_record" "dkim" {
  for_each = local.dkim
  zone_id  = local.zone_id
  name     = "${each.key}._domainkey.example.com"
  type     = "CNAME"
  content  = each.value
  proxied  = false
  ttl      = 3600
}

resource "cloudflare_dns_record" "dmarc" {
  zone_id = local.zone_id
  name    = "_dmarc.example.com"
  type    = "TXT"
  content = "\"v=DMARC1; p=none; rua=mailto:dmarc@example.com\""
  ttl     = 3600
}
```
Provider v4 used `cloudflare_record` with `value` instead of `content` and no quoting of TXT.
Run `tofu plan` and confirm it is not about to delete records created by hand or by another tool.

dnscontrol / octoDNS: both have native `MX`, `TXT`, `CNAME` helpers and will *remove* records not
in code by default; import the existing zone first.

## external-dns and Kubernetes

Clusters running external-dns against the same zone are the main way mail records get destroyed.

- external-dns only manages records that carry its ownership TXT (`heritage=external-dns,...`,
  default prefix `k8s.` or `externaldns-`). Hand-added mail records are safe **unless** `--policy=sync`
  is combined with a `--txt-owner-id` mismatch or `--registry=noop`. Confirm `--policy=upsert-only`
  or that the registry is enabled.
- `--cloudflare-proxied` makes every created record proxied, which breaks DKIM/return-path CNAMEs.
  Do **not** express mail records as `DNSEndpoint` resources in such a cluster; add them by hand
  or via OpenTofu. If they must be in-cluster, annotate
  `external-dns.alpha.kubernetes.io/cloudflare-proxied: "false"` per endpoint.
- `--domain-filter` limits which zones external-dns touches; business domains outside the filter
  are untouched by it, which is desirable for mail.
- cert-manager DNS-01 solvers create and delete `_acme-challenge` TXT records only; they do not
  conflict with mail records but need a token scoped to the zone.

## Generic entry rules for any UI

1. Host/name field: relative (`_dmarc`), not absolute, unless the UI shows the full FQDN and asks
   for it. After saving, `dig` the expected FQDN; if it returns nothing, try the other convention.
2. Apex: `@`, blank, or the bare domain; never `example.com.` *inside* a zone that auto-appends.
3. TXT: paste without outer quotes unless the host documents quoting (Route 53, zone-file editors).
   Look for the UI doubling quotes afterwards.
4. CNAME targets: FQDN; a trailing dot is accepted by most UIs and prevents auto-append.
5. MX: separate priority field; target is a hostname, never an IP.
6. Never leave two SPF records; never leave a CNAME at a name that also needs TXT/MX (CNAME
   excludes all other types at that name).
7. Lower TTL to 300 before a migration, raise to 3600+ afterwards.
8. Verify every record with `dig` or the audit script, from a resolver that has not cached
   (`@ns` authoritative query) and from a public one (`@1.1.1.1`, `@8.8.8.8`).

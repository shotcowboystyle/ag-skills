#!/usr/bin/env bash
# Read-only audit of a domain's mail DNS: NS, MX, SPF (with lookup count), DKIM, DMARC,
# MTA-STS, TLS-RPT, BIMI. Flags the common misconfigurations.
#
# Usage: check_mail_dns.sh <domain> [dkim-selector ...]
#   NS=ns1.example.net  query that server directly (bypass caches right after a change)
#   RESOLVER=1.1.1.1    query a specific recursive resolver (default: system). Use this when the
#                       local resolver truncates large TXT sets or blocks TCP 53 (lookups hang).
#
# Needs: dig (bind-tools / dnsutils), curl (optional, for the MTA-STS policy file).
set -u

domain="${1:?usage: $0 <domain> [dkim-selector ...]}"
shift
domain="${domain%.}"
selectors=("$@")
common_selectors=(google selector1 selector2 fm1 fm2 fm3 protonmail protonmail2 protonmail3
  purelymail1 purelymail2 purelymail3 key1 key2 key3 sig1 zmail default dkim mail k1 k2 k3
  s1 s2 pm resend mandrill mailjet smtp zoho everlytickey1 everlytickey2 cm mxvault)

server=""
if [ -n "${NS:-}" ]; then server="@${NS}"; elif [ -n "${RESOLVER:-}" ]; then server="@${RESOLVER}"; fi

command -v dig >/dev/null || { echo "dig not found (install bind-tools / dnsutils)"; exit 2; }

warn_count=0
ok()   { printf '  OK    %s\n' "$*"; }
warn() { printf '  WARN  %s\n' "$*"; warn_count=$((warn_count+1)); }
info() { printf '  -     %s\n' "$*"; }
q() { dig +short +time=3 +tries=2 +bufsize=4096 $server "$1" "$2" 2>/dev/null; }   # q TYPE name
# TXT records come back as one or more quoted strings per line; join them into one value per line.
txt() { q TXT "$1" | sed -E 's/" +"//g; s/^"//; s/"$//'; }

echo "== $domain  ${server:+(server $server)}"

echo "NS"
ns=$(q NS "$domain")
if [ -z "$ns" ]; then warn "no NS records (domain not delegated, or typo)"; else
  echo "$ns" | sed 's/^/  -     /'
  case "$ns" in
    *cloudflare.com*) info "Cloudflare: make sure DKIM/return-path CNAMEs are DNS only (grey cloud)";;
    *awsdns*)        info "Route 53: TXT values must be quoted in console/API";;
    *registrar-servers.com*) info "Namecheap BasicDNS: Mail Settings must be 'Custom MX'";;
    *domaincontrol.com*) info "GoDaddy DNS";;
    *vercel-dns.com*) info "Vercel DNS";;
    *porkbun.com*)    info "Porkbun DNS";;
  esac
fi

echo "APEX"
if [ -n "$(q CNAME "$domain")" ]; then warn "CNAME at apex; MX/TXT at this name will be ignored"; fi

echo "MX"
mx=$(q MX "$domain")
if [ -z "$mx" ]; then
  warn "no MX: domain cannot receive mail (fine only for a sending-only subdomain or a locked-down domain with null MX)"
else
  echo "$mx" | sort -n | sed 's/^/  -     /'
  if echo "$mx" | grep -qE '^0 \.$'; then info "null MX (RFC 7505): domain declares it accepts no mail"; fi
  echo "$mx" | awk '{print $2}' | grep -v '^\.$' | while read -r host; do
    host="${host%.}"
    if [ -n "$(q CNAME "$host")" ]; then warn "MX target $host is a CNAME (RFC 2181 violation; some receivers reject)"; fi
    if [ -z "$(q A "$host")$(q AAAA "$host")" ]; then warn "MX target $host has no A/AAAA"; fi
    if echo "$host" | grep -qE '^[0-9.]+$'; then warn "MX target $host is an IP address; must be a hostname"; fi
  done
fi

echo "SPF"
spf_lines=$(txt "$domain" | grep -i '^v=spf1')
spf_n=$(printf '%s' "$spf_lines" | grep -c . || true)
if [ "$spf_n" -eq 0 ]; then
  warn "no SPF record"
elif [ "$spf_n" -gt 1 ]; then
  warn "$spf_n SPF records: receivers treat this as permerror (no SPF). Merge into one."
  echo "$spf_lines" | sed 's/^/  -     /'
else
  info "$spf_lines"
  case "$spf_lines" in
    *"redirect="*) info "redirect= present: the 'all' qualifier is evaluated in the redirected record";;
    *"+all"*) warn "+all: anyone may send as this domain";;
    *"-all"*) ok "ends in -all";;
    *"~all"*) ok "ends in ~all (softfail; move to -all once DMARC reports are clean)";;
    *"?all"*) warn "?all is neutral: effectively no policy";;
    *)        warn "no 'all' mechanism; implicit ?all";;
  esac
  echo "$spf_lines" | grep -qiE '(^| )ptr' && warn "ptr mechanism is deprecated"
  if [ -n "$(q SPF "$domain")" ]; then info "legacy SPF RRtype also present (obsolete, harmless)"; fi

  # Count DNS-querying mechanisms recursively (limit 10, RFC 7208 §4.6.4).
  lookups=0; void=0; depth=0; seen=" "
  count_spf() {  # count_spf <domain> <record>
    local d="$1" rec="$2" tok target sub
    depth=$((depth+1))
    [ $depth -gt 20 ] && { warn "SPF include depth > 20, stopping"; return; }
    for tok in $rec; do
      tok="${tok#[+\-~?]}"
      case "$tok" in
        include:*|redirect=*)
          target="${tok#*[:=]}"; lookups=$((lookups+1))
          case "$seen" in *" $target "*) info "   (include:$target seen twice)"; continue;; esac
          seen="$seen$target "
          sub=$(txt "$target" | grep -i '^v=spf1' | head -1)
          if [ -z "$sub" ]; then void=$((void+1)); warn "include:$target has no SPF record (void lookup / permerror)"; else count_spf "$target" "$sub"; fi;;
        a|a:*|mx|mx:*|ptr|ptr:*|exists:*) lookups=$((lookups+1));;
      esac
    done
    depth=$((depth-1))
  }
  count_spf "$domain" "$spf_lines"
  if [ $lookups -gt 10 ]; then warn "SPF needs $lookups DNS lookups (limit 10): permerror"; 
  elif [ $lookups -ge 8 ]; then warn "SPF uses $lookups of 10 lookups; little headroom";
  else ok "SPF uses $lookups of 10 lookups"; fi
  [ $void -gt 2 ] && warn "$void void lookups (limit 2)"
fi

echo "DKIM"
found=0
check_sel() {
  local sel="$1" name="$1._domainkey.$domain" c t
  c=$(q CNAME "$name"); t=$(txt "$name")
  if [ -n "$c" ]; then
    found=$((found+1))
    if [ -n "$t" ]; then ok "$sel -> CNAME ${c%.} (resolves to key)"; else warn "$sel -> CNAME ${c%.} but target yields no TXT (proxied, flattened, or wrong target)"; fi
  elif [ -n "$t" ]; then
    found=$((found+1))
    if echo "$t" | grep -q 'p=' ; then
      if echo "$t" | grep -qE 'p=( |;|$)'; then info "$sel: revoked key (p= empty)"; else ok "$sel: TXT key present ($(echo "$t" | grep -oE 'k=[a-z0-9]+' | head -1 || echo k=rsa))"; fi
      echo "$t" | grep -q 't=y' && warn "$sel: t=y testing flag set; remove in production"
    else warn "$sel: TXT present but no p= tag"; fi
  else
    return 1
  fi
}
for s in ${selectors[@]+"${selectors[@]}"}; do check_sel "$s" || warn "selector '$s' not found"; done
# ponytail: probes a fixed list of common selectors; pass the provider's selectors explicitly for certainty
for s in "${common_selectors[@]}"; do
  skip=0; for g in ${selectors[@]+"${selectors[@]}"}; do [ "$g" = "$s" ] && skip=1; done
  [ $skip -eq 1 ] || check_sel "$s" || true
done
wc_=$(txt "*._domainkey.$domain")
[ -n "$wc_" ] && info "wildcard *._domainkey present: $wc_"
if [ $found -eq 0 ]; then warn "no DKIM selectors found (pass the provider's selectors as arguments to be sure)"; fi

echo "DMARC"
dm=$(txt "_dmarc.$domain" | grep -i '^v=DMARC1')
dm_n=$(printf '%s' "$dm" | grep -c . || true)
dm_cname=$(q CNAME "_dmarc.$domain")
[ -n "$dm_cname" ] && warn "_dmarc is a CNAME to ${dm_cname%.}: you do not control the policy or receive reports"
if [ "$dm_n" -eq 0 ]; then
  warn "no DMARC record"
elif [ "$dm_n" -gt 1 ]; then
  warn "$dm_n DMARC records; receivers ignore all of them"
else
  info "$dm"
  p=$(echo "$dm" | grep -oE 'p=[a-z]+' | head -1 | cut -d= -f2)
  case "$p" in
    none)       info "p=none: monitoring only. Move to quarantine then reject once reports are clean";;
    quarantine) ok "p=quarantine";;
    reject)     ok "p=reject";;
    *)          warn "no valid p= tag";;
  esac
  echo "$dm" | grep -q 'rua=' && ok "rua= present (aggregate reports)" || warn "no rua=: you will never see what fails"
  pct=$(echo "$dm" | grep -oE 'pct=[0-9]+' | cut -d= -f2); [ -n "$pct" ] && [ "$pct" != "100" ] && info "pct=$pct: policy applies to $pct% of failing mail"
  echo "$dm" | grep -q 'sp=' || info "no sp=: subdomains inherit p=$p"
  for addr in $(echo "$dm" | grep -oE 'mailto:[^,; ]+' | cut -d: -f2); do
    rd="${addr#*@}"
    if [ "$rd" != "$domain" ] && ! echo "$domain" | grep -q "\.$rd$"; then
      auth=$(txt "$domain._report._dmarc.$rd" | grep -i 'v=DMARC1')
      [ -z "$auth" ] && warn "reports to $addr: $rd has no $domain._report._dmarc.$rd authorization record (reports may not be sent)"
    fi
  done
fi

echo "MTA-STS / TLS-RPT"
sts=$(txt "_mta-sts.$domain" | grep -i '^v=STSv1')
if [ -n "$sts" ]; then
  info "$sts"
  if command -v curl >/dev/null; then
    pol=$(curl -fsS --max-time 5 "https://mta-sts.$domain/.well-known/mta-sts.txt" 2>/dev/null)
    if [ -n "$pol" ]; then
      mode=$(echo "$pol" | grep -i '^mode:' | awk '{print $2}')
      ok "policy served, mode=$mode"
      # ponytail: suffix match approximates MTA-STS wildcard rules; exact RFC 8461 matching if it ever misfires
      for h in $(echo "$mx" | awk '{print $2}' | sed 's/\.$//'); do
        echo "$pol" | grep -qiE "^mx: *(\*\.)?${h#*.}|^mx: *$h" || warn "MX $h not matched by MTA-STS policy"
      done
    else warn "TXT present but https://mta-sts.$domain/.well-known/mta-sts.txt not reachable"; fi
  fi
else info "no MTA-STS (optional)"; fi
tlsrpt=$(txt "_smtp._tls.$domain" | grep -i '^v=TLSRPTv1')
[ -n "$tlsrpt" ] && info "$tlsrpt" || info "no TLS-RPT (optional)"

echo "BIMI"
bimi=$(txt "default._bimi.$domain" | grep -i '^v=BIMI1')
if [ -n "$bimi" ]; then
  info "$bimi"
  [ "$p" = "none" ] && warn "BIMI requires DMARC quarantine/reject"
else info "no BIMI (optional)"; fi

echo "CLIENT CONFIG"
for n in autoconfig autodiscover; do c=$(q CNAME "$n.$domain"); [ -n "$c" ] && info "$n -> ${c%.}"; done
for n in _imaps._tcp _submission._tcp _submissions._tcp _autodiscover._tcp; do s=$(q SRV "$n.$domain"); [ -n "$s" ] && info "$n SRV $s"; done

echo "== $warn_count warning(s)"
[ $warn_count -eq 0 ]

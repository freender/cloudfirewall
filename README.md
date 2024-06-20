# cloudfirewall

Personal agent to update an IP address in WAF firewall rule if hosts IP changes


Docker Compose:
```
version: '3'

services:
  cloudfirewall:
    image: ghcr.io/freender/cloudfirewall:main
    #build: https://github.com/freender/cloudfirewall.git
    container_name: cloudfirewall
    environment:
      - WAF_TOKEN=${WAF_TOKEN} # Cloudflare WAF token
      - WAF_ZONE=${WAF_ZONE} # Cloudflare WAF zone
      - WAF_RULESET=${WAF_RULESET} # Cloudflare WAF ruleset
      - WAF_RULEID=${WAF_RULEID} # Cloudflare WAF rule id
```

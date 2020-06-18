#!/bin/sh
cd /tmp
wget https://www.cloudflare.com/ips-v4 -O ips-v4-$$.tmp
wget https://www.cloudflare.com/ips-v6 -O ips-v6-$$.tmp

for cfip in `cat ips-v4-$$.tmp`; do echo "ufw allow from $cfip to any port 443 proto tcp"; done
for cfip in `cat ips-v6-$$.tmp`; do echo "ufw allow from $cfip to any port 443 proto tcp"; done

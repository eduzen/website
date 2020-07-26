#!/bin/sh
cd /tmp
wget https://www.cloudflare.com/ips-v4 -O ips-v4-$$.tmp
wget https://www.cloudflare.com/ips-v6 -O ips-v6-$$.tmp

for cfip in `cat ips-v4-$$.tmp`; do ufw allow from $cfip to any port 80 proto tcp; done
for cfip in `cat ips-v6-$$.tmp`; do ufw allow from $cfip to any port 80 proto tcp; done

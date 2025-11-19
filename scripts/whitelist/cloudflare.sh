#!/bin/bash
cd /tmp

wget https://www.cloudflare.com/ips-v4 -O ips-v4-$$.tmp;
wget https://www.cloudflare.com/ips-v6 -O ips-v6-$$.tmp;

for cfip in $(cat ips-v4-$$.tmp); do
    ufw route allow proto tcp from $cfip to any port 80;
    ufw route allow proto tcp from $cfip to any port 443;
done

for cfip in $(cat ips-v6-$$.tmp); do
    ufw route allow proto tcp from $cfip to any port 80;
    ufw route allow proto tcp from $cfip to any port 443;
done

# Allow SSH from anywhere (or restrict this to your VPN/IP)
ufw allow ssh;

# Reload UFW to apply changes
ufw reload;

# Clean up temporary files
rm ips-v4-$$.tmp ips-v6-$$.tmp;

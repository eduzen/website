#!/bin/sh

cd /tmp
http https://www.cloudflare.com/ips-v4 > ips-v4.tmp
http https://www.cloudflare.com/ips-v6 > ips-v6.tmp

for cfip in $(cat ips-v4.tmp);
  do echo $cfip;
  # do ufw allow from $cfip to any port 80 proto tcp;
done

for cfip in $(cat ips-v6.tmp);
  do echo $cfip;
  # do ufw allow from $cfip to any port 80 proto tcp;
done

if [ -f ips-v4.tmp ]; then
   rm ips-v4.tmp
fi

if [ -f ips-v6.tmp ]; then
   rm ips-v6.tmp
fi

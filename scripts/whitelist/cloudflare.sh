#!/bin/bash
cd /tmp

wget https://www.cloudflare.com/ips-v4 -O ips-v4-$$.tmp;
wget https://www.cloudflare.com/ips-v6 -O ips-v6-$$.tmp;

for cfip in `cat ips-v4-$$.tmp`; do
  ufw allow from $cfip to any port 443 proto tcp;
  ufw allow from $cfip to any port 80 proto tcp;
  ufw route allow proto tcp from $cfip to any port 80;
done

for cfip in `cat ips-v6-$$.tmp`; do
  ufw allow from $cfip to any port 443 proto tcp;
  ufw allow from $cfip to any port 80 proto tcp;
  ufw route allow proto tcp from $cfip to any port 80
done

ufw allow ssh;
ufw deny http;
ufw deny https;

echo "# BEGIN UFW AND DOCKER
*filter
:ufw-user-forward - [0:0]
:ufw-docker-logging-deny - [0:0]
:DOCKER-USER - [0:0]
-A DOCKER-USER -j ufw-user-forward

-A DOCKER-USER -j RETURN -s 10.0.0.0/8
-A DOCKER-USER -j RETURN -s 172.16.0.0/12
-A DOCKER-USER -j RETURN -s 192.168.0.0/16

-A DOCKER-USER -p udp -m udp --sport 53 --dport 1024:65535 -j RETURN

-A DOCKER-USER -j ufw-docker-logging-deny -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -d 192.168.0.0/16
-A DOCKER-USER -j ufw-docker-logging-deny -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -d 10.0.0.0/8
-A DOCKER-USER -j ufw-docker-logging-deny -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -d 172.16.0.0/12
-A DOCKER-USER -j ufw-docker-logging-deny -p udp -m udp --dport 0:32767 -d 192.168.0.0/16
-A DOCKER-USER -j ufw-docker-logging-deny -p udp -m udp --dport 0:32767 -d 10.0.0.0/8
-A DOCKER-USER -j ufw-docker-logging-deny -p udp -m udp --dport 0:32767 -d 172.16.0.0/12

-A DOCKER-USER -j RETURN

-A ufw-docker-logging-deny -m limit --limit 3/min --limit-burst 10 -j LOG --log-prefix \"[UFW DOCKER BLOCK] \"
-A ufw-docker-logging-deny -j DROP

COMMIT
# END UFW AND DOCKER" >> /etc/ufw/after.rules;

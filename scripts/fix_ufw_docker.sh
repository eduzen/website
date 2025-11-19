#!/bin/bash
set -e

RULES_FILE="/etc/ufw/after.rules"
BACKUP_FILE="${RULES_FILE}.bak_$(date +%s)"

echo "[-] Backing up ${RULES_FILE} to ${BACKUP_FILE}..."
cp "$RULES_FILE" "$BACKUP_FILE"

# 1. Sanitize: Remove any existing blocks created by the previous script
# This sed command deletes any lines between the markers (inclusive), handling multiple occurrences.
echo "[-] Cleaning up old/duplicate Docker blocks..."
sed -i '/# BEGIN UFW AND DOCKER/,/# END UFW AND DOCKER/d' "$RULES_FILE"

# 2. Patch: Append the correct logic for Cloudflare/Docker routing
# We check ufw-user-forward (where 'ufw route' rules live) before dropping 80/443.
echo "[-] Appending new DOCKER-USER chain logic..."

cat <<EOT >> "$RULES_FILE"

# BEGIN UFW AND DOCKER
*filter
:DOCKER-USER - [0:0]
:ufw-user-forward - [0:0]

# 1. Allow internal networks (Containers talking to each other or host)
-A DOCKER-USER -s 10.0.0.0/8 -j RETURN
-A DOCKER-USER -s 172.16.0.0/12 -j RETURN
-A DOCKER-USER -s 192.168.0.0/16 -j RETURN

# 2. Check UFW Route Rules
# This passes packets to the chain where 'ufw route allow' rules exist.
# If a packet matches a Cloudflare IP here, it is ACCEPTED and stops processing.
-A DOCKER-USER -j ufw-user-forward

# 3. Block External Web Traffic that wasn't accepted above
# If we are here, it wasn't a Cloudflare IP (or explicitly allowed route).
-A DOCKER-USER -p tcp -m tcp --dport 80 -j DROP
-A DOCKER-USER -p tcp -m tcp --dport 443 -j DROP

# 4. Default: Return to Docker (allows everything else not explicitly dropped)
-A DOCKER-USER -j RETURN

COMMIT
# END UFW AND DOCKER
EOT

echo "[-] Reloading UFW..."
ufw reload

echo "[+] Done. Docker traffic on 80/443 is now locked to your UFW route rules."

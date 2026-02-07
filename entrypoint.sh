#!/bin/sh

# Initialiser un fichier config vide pour que Privoxy ne crash pas au boot
echo "listen-address 127.0.0.1:8118" > /etc/privoxy/config

# Lancer Privoxy en background
privoxy --no-daemon /etc/privoxy/config &

# Attendre 2 secondes et faire le premier update
sleep 2
python3 /usr/local/bin/update_proxies.py

# Boucle d'update toutes les 5 minutes en arrière-plan
(
  while true; do
    sleep 300
    python3 /usr/local/bin/update_proxies.py
  done
) &

# Lancer SearXNG (le script original de l'image)
exec /usr/local/bin/docker-entrypoint.sh

#!/bin/sh

# Lancer Privoxy en arrière-plan
privoxy --no-daemon /etc/privoxy/config &

# Premier update des proxys
python3 /usr/local/bin/update_proxies.py

# Boucle d'update infinie toutes les 5min (300s)
(
  while true; do
    sleep 300
    python3 /usr/local/bin/update_proxies.py
  done
) &

# Lancer SearXNG (le processus principal)
/usr/local/bin/docker-entrypoint.sh

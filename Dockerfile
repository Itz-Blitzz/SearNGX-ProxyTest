FROM searxng/searxng:latest

# Installation des outils nécessaires
USER root
RUN apk add --no-cache privoxy python3 procps

# Copie des fichiers de config
COPY settings.yml /etc/searxng/settings.yml
COPY update_proxies.py /usr/local/bin/update_proxies.py
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /usr/local/bin/update_proxies.py /entrypoint.sh

# On expose le port de SearXNG
EXPOSE 8080

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]

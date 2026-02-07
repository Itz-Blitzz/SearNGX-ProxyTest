FROM searxng/searxng:latest

USER root

# Installation des dépendances
RUN apt-get update && apt-get install -y \
    privoxy \
    python3 \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers
COPY settings.yml /etc/searxng/settings.yml
COPY update_proxies.py /usr/local/bin/update_proxies.py
COPY entrypoint.sh /entrypoint.sh

# Permissions
RUN chmod +x /usr/local/bin/update_proxies.py /entrypoint.sh
RUN chown -R searxng:searxng /etc/privoxy

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]

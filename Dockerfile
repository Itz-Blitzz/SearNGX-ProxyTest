FROM searxng/searxng:latest

USER root

# On copie juste nos fichiers (pas de RUN apt ou apk !)
COPY settings.yml /etc/searxng/settings.yml
COPY rotary_proxy.py /usr/local/bin/rotary_proxy.py

# On crée un script de lancement simple
RUN echo '#!/bin/sh\n\
python3 /usr/local/bin/rotary_proxy.py &\n\
exec /usr/local/bin/docker-entrypoint.sh' > /entrypoint_custom.sh && \
chmod +x /entrypoint_custom.sh

EXPOSE 8080

ENTRYPOINT ["/bin/sh", "/entrypoint_custom.sh"]

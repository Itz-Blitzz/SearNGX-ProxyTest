FROM searxng/searxng:latest

# On copie ton fichier de configuration dans le dossier de SearXNG
COPY settings.yml /etc/searxng/settings.yml

# Pas besoin de plus, l'image de base gère déjà le démarrage

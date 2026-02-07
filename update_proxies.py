import urllib.request
import json
import subprocess
import os

URL = "https://raw.githubusercontent.com/mishableskineetudiant-stack/proxylistfiltered/refs/heads/main/proxies_elite.json"
CONFIG_PATH = "/etc/privoxy/config"

def update():
    try:
        with urllib.request.urlopen(URL) as response:
            data = json.loads(response.read().decode())
            proxies = data.get("proxies", [])
            
        # On trie par response_time (le plus petit d'abord)
        proxies.sort(key=lambda x: x.get('response_time', 999))
        
        # On prend les 15 meilleurs pour garder une bonne performance
        top_proxies = proxies[:15]
            
        with open(CONFIG_PATH, "w") as f:
            f.write("listen-address 127.0.0.1:8118\n")
            f.write("forwarded-connect-retries 3\n")
            f.write("keep-alive-timeout 5\n")
            f.write("max-client-connections 256\n")
            
            for p in top_proxies:
                ip = p['ip']
                port = p['port']
                # Privoxy utilise "forward" pour HTTP et "forward-socks5" pour SOCKS
                f.write(f"forward / {ip}:{port}\n")
        
        # On dit à Privoxy de recharger la config
        subprocess.run(["pkill", "-HUP", "privoxy"])
        print(f"Update success: {len(top_proxies)} proxies loaded.")
    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    update()

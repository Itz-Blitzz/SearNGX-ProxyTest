import urllib.request
import json
import os
import subprocess

URL = "https://raw.githubusercontent.com/mishableskineetudiant-stack/proxylistfiltered/refs/heads/main/proxies_elite.json"
CONFIG_PATH = "/etc/privoxy/config"

def update():
    try:
        with urllib.request.urlopen(URL) as response:
            data = json.loads(response.read().decode())
            proxies = data.get("proxies", [])[:20] # On prend les 20 premiers pour la stabilité
            
        with open(CONFIG_PATH, "w") as f:
            f.write("listen-address 127.0.0.1:8118\n")
            f.write("forwarded-connect-retries 2\n")
            f.write("keep-alive-timeout 5\n")
            # On ajoute chaque proxy comme une règle de forward
            for p in proxies:
                line = f"forward / {p['ip']}:{p['port']}\n"
                f.write(line)
        
        # On demande à Privoxy de relire sa config (Signal HUP)
        subprocess.run(["pkill", "-HUP", "privoxy"])
        print("Proxies updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update()

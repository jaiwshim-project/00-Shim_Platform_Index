# -*- coding: utf-8 -*-
"""
프로젝트 인덱스 로컬 서버
실행: python serve.py
접속: http://localhost:9999
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from http.server import HTTPServer, SimpleHTTPRequestHandler
import subprocess, urllib.parse, os

ROOT = os.path.dirname(os.path.abspath(__file__))

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == '/open':
            params = urllib.parse.parse_qs(parsed.query)
            path = params.get('path', [''])[0]
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            if path and path != '__check__' and os.path.exists(path):
                subprocess.Popen(['explorer', os.path.normpath(path)])
                self.wfile.write(b'ok')
            else:
                self.wfile.write(b'ok')
            return

        super().do_GET()

    def log_message(self, fmt, *args):
        pass  # 로그 숨김

PORT = 9999
os.chdir(ROOT)

print('=' * 45)
print('  Project Index Server')
print('  http://localhost:{}'.format(PORT))
print('  Stop: Ctrl+C')
print('=' * 45)

try:
    HTTPServer(('localhost', PORT), Handler).serve_forever()
except KeyboardInterrupt:
    print('Server stopped.')
    sys.exit(0)

#!/usr/bin/env python3
import os
import socket
import threading
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
import base64
import select

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

PROXY_USERNAME = os.getenv('PROXY_USERNAME', 'proxyuser')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD', 'changeme')
PORT = int(os.getenv('PORT', '80'))
class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_CONNECT(self):
        self.handle_connect()

    def handle_connect(self):
        """Handle CONNECT method for HTTPS tunneling"""
        if not self.check_auth():
            return
        
        try:
            host, port = self.path.split(':')
            port = int(port)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            
            self.send_response(200, 'Connection established')
            self.end_headers()
            
            self.connection.setblocking(False)
            sock.setblocking(False)
            
            self.tunnel(sock)
        except Exception as e:
            logger.error(f'CONNECT error: {e}')
            self.send_response(500)
            self.end_headers()

    def handle_request(self):
        """Handle HTTP request proxying"""
        if not self.check_auth():
            return
        
        try:
            if self.path.startswith('http'):
                url = self.path
            else:
                url = f'http://{self.headers.get("Host")}{self.path}'
            
            logger.info(f'Proxy request: {self.command} {url}')
            
            headers = dict(self.headers)
            headers.pop('Host', None)
            headers.pop('Proxy-Connection', None)
            
            req = urllib.request.Request(url, headers=headers, method=self.command)
            
            if self.command in ['POST', 'PUT', 'PATCH']:
                content_length = self.headers.get('Content-Length')
                if content_length:
                    body = self.rfile.read(int(content_length))
                    req.data = body
            
            try:
                response = urllib.request.urlopen(req, timeout=30)
                self.send_response(response.code)
                
                for header, value in response.headers.items():
                    self.send_header(header, value)
                self.end_headers()
                
                while True:
                    data = response.read(4096)
                    if not data:
                        break
                    self.wfile.write(data)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Error: {e.reason}'.encode())
        except Exception as e:
            logger.error(f'Request error: {e}')
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())

    def check_auth(self):
        """Check proxy authentication"""
        auth = self.headers.get('Proxy-Authorization')
        if not auth:
            self.send_response(407)
            self.send_header('Proxy-Authenticate', 'Basic realm="Proxy"')
            self.end_headers()
            return False
        
        try:
            import base64
            auth_type, auth_data = auth.split(' ', 1)
            if auth_type.lower() != 'basic':
                return False
            
            username, password = base64.b64decode(auth_data).decode().split(':', 1)
            if username == PROXY_USERNAME and password == PROXY_PASSWORD:
                logger.info(f'Auth success: {username}')
                return True
            else:
                logger.warning(f'Auth failed: {username}')
                self.send_response(407)
                self.send_header('Proxy-Authenticate', 'Basic realm="Proxy"')
                self.end_headers()
                return False
        except Exception as e:
            logger.error(f'Auth error: {e}')
            self.send_response(407)
            self.send_header('Proxy-Authenticate', 'Basic realm="Proxy"')
            self.end_headers()
            return False

    def tunnel(self, sock):
        """Tunnel data between client and server"""
        import select
        try:
            while True:
                readable, _, _ = select.select([self.connection, sock], [], [])
                for s in readable:
                    data = s.recv(4096)
                    if not data:
                        return
                    other = sock if s == self.connection else self.connection
                    other.sendall(data)
        except Exception as e:
            logger.error(f'Tunnel error: {e}')

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), ProxyHandler)
    logger.info(f'HTTP Proxy listening on port {PORT}')
    logger.info(f'Credentials: {PROXY_USERNAME}:{PROXY_PASSWORD}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info('Shutting down')
        server.shutdown()

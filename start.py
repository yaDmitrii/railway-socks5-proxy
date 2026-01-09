#!/usr/bin/env python3
import socket
import threading
import struct
import select
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

import os
USERNAME = os.getenv('PROXY_USERNAME', 'proxyuser').encode()
PORT = 1080
PASSWORD = os.getenv('PROXY_PASSWORD', 'changeme').encode()

def handle_socks5(client_socket, addr):
    try:
        # SOCKS5 greeting
        data = client_socket.recv(1024)
        if not data or data[0] != 5:
            client_socket.close()
            return
        
        nmethods = data[1]
        # Send selection of auth method (username/password = 2)
        client_socket.sendall(b'\x05\x02')
        
        # Auth phase
        auth_data = client_socket.recv(1024)
        if auth_data[0] == 1:  # username/password auth
            ulen = auth_data[1]
            username = auth_data[2:2+ulen]
            plen = auth_data[2+ulen]
            password = auth_data[2+ulen+1:2+ulen+1+plen]
            
            if username == USERNAME and password == PASSWORD:
                client_socket.sendall(b'\x01\x00')  # Auth success
            else:
                client_socket.sendall(b'\x01\x01')  # Auth failure
                client_socket.close()
                return
        
        # Connection request
        req = client_socket.recv(1024)
        if req[1] == 1:  # CONNECT
            atyp = req[3]
            if atyp == 1:  # IPv4
                addr_bytes = req[4:8]
                port_bytes = req[8:10]
                target_addr = '.'.join(str(b) for b in addr_bytes)
                target_port = struct.unpack('>H', port_bytes)[0]
            elif atyp == 3:  # Domain
                alen = req[4]
                addr_bytes = req[5:5+alen]
                port_bytes = req[5+alen:5+alen+2]
                target_addr = addr_bytes.decode()
                target_port = struct.unpack('>H', port_bytes)[0]
            else:
                client_socket.sendall(b'\x05\x07\x00\x01\x00\x00\x00\x00\x00\x00')
                client_socket.close()
                return
            
            try:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.connect((target_addr, target_port))
                logger.info(f'Connected to {target_addr}:{target_port} from {addr}')
                
                # Success response
                client_socket.sendall(b'\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00')
                
                # Relay data
                relay(client_socket, server)
                server.close()
            except Exception as e:
                logger.error(f'Connection failed: {e}')
                client_socket.sendall(b'\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00')
                client_socket.close()
        else:
            client_socket.sendall(b'\x05\x07\x00\x01\x00\x00\x00\x00\x00\x00')
            client_socket.close()
    except Exception as e:
        logger.error(f'Error: {e}')
        try:
            client_socket.close()
        except:
            pass

def relay(client, server):
    while True:
        try:
            r, _, _ = select.select([client, server], [], [])
            for sock in r:
                data = sock.recv(4096)
                if not data:
                    return
                other = server if sock == client else client
                other.sendall(data)
        except Exception as e:
            logger.error(f'Relay error: {e}')
            return

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', PORT))
    server.listen(5)
    logger.info(f'SOCKS5 proxy listening on port {PORT}')
    
    try:
        while True:
            client, addr = server.accept()
            logger.info(f'New connection from {addr}')
            thread = threading.Thread(target=handle_socks5, args=(client, addr))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        logger.info('Shutting down')
    finally:
        server.close()

if __name__ == '__main__':
    main()

#!/bin/bash
set -e

# Update password for proxyuser from Railway environment variable
if [ -n "$PROXY_PASSWORD" ]; then
  echo "proxyuser:$PROXY_PASSWORD" | chpasswd
fi

# Start dante SOCKS5 proxy server
exec danted -f /etc/danted.conf 

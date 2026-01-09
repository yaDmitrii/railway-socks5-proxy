#!/bin/bash
set -e

# Update password for proxyuser from environment variable
if [ -n "$PROXY_PASSWORD" ]; then
  echo "proxyuser:$PROXY_PASSWORD" | chpasswd
fi

# Get the container's IP address and inject it into danted.conf
# This ensures Dante knows which address to use for outbound connections
CONTAINER_IP=$(hostname -I | awk '{print $1}')
if [ -z "$CONTAINER_IP" ]; then
  echo "Error: Could not determine container IP address"
  exit 1
fi

echo "Detected container IP: $CONTAINER_IP"
sed -i "3a external: $CONTAINER_IP" /etc/danted.conf

echo "Starting Dante SOCKS5 server..."
exec danted -f /etc/danted.conf

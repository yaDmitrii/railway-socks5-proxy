#!/bin/bash
set -e

# Set the password for proxyuser
echo "proxyuser:${PROXY_PASSWORD:-changeme}" | chpasswd

# Start danted
exec danted -f /etc/danted.conf

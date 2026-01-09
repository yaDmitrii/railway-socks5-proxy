FROM python:3.11-alpine

WORKDIR /app

# Install dante-server for SOCKS5 proxy
RUN apk add --no-cache dante-server bash

# Install Python dependencies
RUN pip install --no-cache-dir pysocks

# Create proxyuser for dante
RUN adduser -D -s /bin/false proxyuser && \
    echo "proxyuser:changeme" | chpasswd

# Copy configuration files
COPY danted.conf /etc/danted.conf
COPY entrypoint.sh /app/entrypoint.sh

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

EXPOSE 1080

ENTRYPOINT ["/app/entrypoint.sh"]

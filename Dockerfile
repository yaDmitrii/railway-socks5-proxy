FROM debian:12-slim

WORKDIR /app

# Install dante-server and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    dante-server \
    bash \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create proxyuser for dante
RUN useradd -m -s /bin/false proxyuser && \
    echo "proxyuser:changeme" | chpasswd

# Copy configuration files
COPY danted.conf /etc/danted.conf
COPY entrypoint.sh /app/entrypoint.sh

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

EXPOSE 1080

ENTRYPOINT ["/app/entrypoint.sh"]

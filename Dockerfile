FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y dante-server && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m proxyuser && \
    echo "proxyuser:changeme" | chpasswd

COPY danted.conf /etc/danted.conf

EXPOSE 1080

CMD ["danted", "-f", "/etc/danted.conf"]

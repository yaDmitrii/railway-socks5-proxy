FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y dante-server && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m proxyuser

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY danted.conf /etc/danted.conf

EXPOSE 1080

ENTRYPOINT ["/entrypoint.sh"]

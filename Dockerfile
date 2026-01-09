FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y dante-server && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY danted.conf /etc/danted.conf

EXPOSE 1080

CMD ["danted", "-D", "-f", "/etc/danted.conf"]

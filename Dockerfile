FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y dante-server && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ARG PROXY_PASSWORD=change_me_in_railway_env

RUN useradd -m proxyuser && echo "proxyuser:${PROXY_PASSWORD}" | chpasswd

COPY danted.conf /etc/danted.conf

EXPOSE 1080

CMD ["danted", "-f", "/etc/danted.conf"]

FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y dante-server && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ARG PROXY_PASSWORD=Wtf1!Pusy

RUN useradd -m proxyuser && echo "proxyuser:${PROXY_PASSWORD}" | chpasswd

COPY danted.conf /etc/danted.conf

EXPOSE 1080

CMD ["danted", "-D", "-F", "/etc/danted.conf"]

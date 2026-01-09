FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache bash

RUN pip install --no-cache-dir pysocks

RUN adduser -D proxyuser && \
    echo "proxyuser:changeme" | chpasswd 2>/dev/null || true

COPY start.py .

EXPOSE 1080

CMD ["python", "start.py"]

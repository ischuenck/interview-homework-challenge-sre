FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends iproute2 procps \
    && rm -rf /var/lib/apt/lists/*

COPY challenge-3/server.py .
COPY challenge-2/system-info.py .

RUN chmod +x server.py
RUN chmod +x system-info.py

EXPOSE 8080

CMD ["python", "server.py"]

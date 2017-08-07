FROM resin/raspberry-pi-debian:jessie

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    python \
    python3 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

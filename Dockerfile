FROM resin/raspberry-pi-debian:jessie

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    python \
    build-essential \
    python-dev \
    python-smbus \
    python-pip \
    i2c-tools \
    ModemManager \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install adafruit-ads1x15

COPY . .

CMD python app/main.py

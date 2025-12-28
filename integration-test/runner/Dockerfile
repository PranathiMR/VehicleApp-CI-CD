FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y \
      mosquitto-clients \
      netcat-openbsd \
      ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /test
COPY test.sh .

CMD ["./test.sh"]

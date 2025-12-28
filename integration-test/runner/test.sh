#!/bin/sh
set -e

BROKER_HOST=seat-adjuster
BROKER_PORT=1883

REQUEST_TOPIC="seatadjuster/setPosition/request"
RESPONSE_TOPIC="seatadjuster/setPosition/response"

REQUEST_ID=1
POSITION=42

echo "Waiting for MQTT broker..."
until nc -z ${BROKER_HOST} ${BROKER_PORT}; do
  sleep 1
done

echo "MQTT broker is reachable"

echo "Listening for response..."
mosquitto_sub \
  -h ${BROKER_HOST} \
  -p ${BROKER_PORT} \
  -t ${RESPONSE_TOPIC} \
  > /tmp/response.json &
SUB_PID=$!

sleep 1

echo "Publishing request..."
mosquitto_pub \
  -h ${BROKER_HOST} \
  -p ${BROKER_PORT} \
  -t ${REQUEST_TOPIC} \
  -m "{\"requestId\":${REQUEST_ID},\"position\":${POSITION}}"

sleep 3
kill ${SUB_PID}

echo "Received response:"
cat /tmp/response.json

grep "\"status\":0" /tmp/response.json
grep "\"Set Seat position to: ${POSITION}\"" /tmp/response.json

echo "✅ Integration test PASSED"

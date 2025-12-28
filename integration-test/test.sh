#!/bin/sh
set -e

echo "Waiting for Kuksa Databroker..."

until nc -z kuksa-databroker 55555; do
  sleep 1
done

echo "Kuksa Databroker is reachable"
echo "Phase 1 integration test PASSED"

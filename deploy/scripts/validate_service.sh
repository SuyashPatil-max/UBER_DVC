#!/bin/bash
# CodeDeploy ValidateService hook.
# Polls the local /health endpoint so CodeDeploy only marks the deployment
# (and this instance, under the ASG's rolling deployment) successful once the
# container is actually serving traffic. A failure here fails the deployment.
set -uo pipefail

HEALTH_URL="http://127.0.0.1:8002/health"
MAX_RETRIES=10
SLEEP_SECONDS=5

echo "==> [ValidateService] Checking ${HEALTH_URL}"

for attempt in $(seq 1 "${MAX_RETRIES}"); do
  if curl --fail --silent --max-time 5 "${HEALTH_URL}" >/dev/null; then
    echo "==> [ValidateService] Healthy on attempt ${attempt}/${MAX_RETRIES}"
    exit 0
  fi
  echo "==> [ValidateService] Attempt ${attempt}/${MAX_RETRIES} failed, retrying in ${SLEEP_SECONDS}s"
  sleep "${SLEEP_SECONDS}"
done

echo "==> [ValidateService] Service failed to become healthy after ${MAX_RETRIES} attempts"
exit 1

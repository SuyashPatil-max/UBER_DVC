#!/bin/bash
# CodeDeploy ApplicationStop hook.
# Stops and removes the currently running container (if any) so the port is
# free for the new one. Must not fail on a fresh instance that has nothing
# running yet — CodeDeploy runs this hook even on the very first deployment.
set -uo pipefail

CONTAINER_NAME="uber-backend"

echo "==> [ApplicationStop] Looking for existing container: ${CONTAINER_NAME}"

if docker ps -a --format '{{.Names}}' | grep -Fxq "${CONTAINER_NAME}"; then
  echo "==> [ApplicationStop] Stopping ${CONTAINER_NAME}"
  docker stop "${CONTAINER_NAME}" || true
  echo "==> [ApplicationStop] Removing ${CONTAINER_NAME}"
  docker rm "${CONTAINER_NAME}" || true
else
  echo "==> [ApplicationStop] No existing container found, nothing to stop"
fi

exit 0

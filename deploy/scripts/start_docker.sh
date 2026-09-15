set -euo pipefail

AWS_REGION="eu-north-1"
ECR_REGISTRY="942091278141.dkr.ecr.eu-north-1.amazonaws.com"
IMAGE_NAME="uber-backend"
IMAGE_TAG="latest"
CONTAINER_NAME="uber-backend"
HOST_PORT=8002
CONTAINER_PORT=8002

echo "==> [ApplicationStart] Logging in to ECR (${ECR_REGISTRY})"
aws ecr get-login-password --region "${AWS_REGION}" \
  | docker login --username AWS --password-stdin "${ECR_REGISTRY}"

echo "==> [ApplicationStart] Pulling ${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
docker pull "${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"

echo "==> [ApplicationStart] Starting container ${CONTAINER_NAME}"
docker run -d \
  --name "${CONTAINER_NAME}" \
  --restart unless-stopped \
  -p "${HOST_PORT}:${CONTAINER_PORT}" \
  "${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"


docker image prune -f || true

docker ps --filter "name=${CONTAINER_NAME}"
echo "==> [ApplicationStart] Container started"

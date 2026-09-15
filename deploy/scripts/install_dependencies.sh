#!/bin/bash
# CodeDeploy BeforeInstall hook.
# Makes sure Docker and the AWS CLI are present on the instance before we try
# to pull/run anything. Idempotent so it's safe on every deployment.
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

echo "==> [BeforeInstall] Updating apt cache"
apt-get update -y

if ! command -v docker >/dev/null 2>&1; then
  echo "==> [BeforeInstall] Docker not found, installing docker.io"
  apt-get install -y docker.io
fi

systemctl enable docker
systemctl start docker

# Let the default 'ubuntu' user run docker without sudo (harmless if it already can)
if id "ubuntu" >/dev/null 2>&1; then
  usermod -aG docker ubuntu || true
fi

if ! command -v aws >/dev/null 2>&1; then
  echo "==> [BeforeInstall] AWS CLI not found, installing"
  apt-get install -y unzip curl
  curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
  unzip -q -o /tmp/awscliv2.zip -d /tmp
  /tmp/aws/install --update
  rm -rf /tmp/awscliv2.zip /tmp/aws
fi

echo "==> [BeforeInstall] docker: $(docker --version)"
echo "==> [BeforeInstall] aws-cli: $(aws --version)"
echo "==> [BeforeInstall] Dependencies ready"

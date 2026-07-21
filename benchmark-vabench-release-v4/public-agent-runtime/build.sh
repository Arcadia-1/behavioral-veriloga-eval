#!/bin/sh
set -eu

cd "$(dirname "$0")"

IMAGE_TAG="${IMAGE_TAG:-vabench-agent-runtime:0.8.3}"
PLATFORM="${PLATFORM:-linux/amd64}"
DOCKER="${DOCKER:-docker}"

"$DOCKER" buildx build \
    --platform "$PLATFORM" \
    --pull \
    --load \
    --tag "$IMAGE_TAG" \
    .

"$DOCKER" image inspect "$IMAGE_TAG" --format '{{.Id}}'

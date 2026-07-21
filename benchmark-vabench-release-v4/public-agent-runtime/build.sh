#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)

IMAGE_TAG="${IMAGE_TAG:-vabench-agent-runtime:0.8.3}"
PLATFORM="${PLATFORM:-linux/amd64}"
DOCKER="${DOCKER:-docker}"

"$DOCKER" buildx build \
    --platform "$PLATFORM" \
    --pull \
    --load \
    --tag "$IMAGE_TAG" \
    "$REPO_ROOT/environment"

"$DOCKER" image inspect "$IMAGE_TAG" --format '{{.Id}}'

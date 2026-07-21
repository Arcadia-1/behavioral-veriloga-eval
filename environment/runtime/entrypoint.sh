#!/bin/sh
set -eu

if [ ! -d /workspace/public/task ]; then
    echo "missing read-only task mount: /workspace/public/task" >&2
    exit 64
fi
if [ ! -d /workspace/public/submission ]; then
    echo "missing writable submission mount: /workspace/public/submission" >&2
    exit 64
fi
if [ ! -d /workspace/work ]; then
    echo "missing writable work mount: /workspace/work" >&2
    exit 64
fi

exec "$@"

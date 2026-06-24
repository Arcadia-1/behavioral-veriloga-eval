#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_ROOT="$(cd "$ROOT_DIR/.." && pwd)"
DEFAULT_BRIDGE_REPO="$PROJECT_ROOT/../iccad/virtuoso-bridge-lite"
BRIDGE_REPO="${BRIDGE_REPO:-$DEFAULT_BRIDGE_REPO}"
BRIDGE_ENV="${BRIDGE_ENV:-$BRIDGE_REPO/.env}"

if [[ ! -f "$BRIDGE_ENV" ]]; then
  echo "bridge env not found: $BRIDGE_ENV" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "$BRIDGE_ENV"
set +a

BRIDGE_PROFILE="${BRIDGE_PROFILE:-}"
apply_bridge_profile() {
  if [[ -z "$BRIDGE_PROFILE" ]]; then
    return
  fi
  local key profiled
  for key in VB_REMOTE_HOST VB_REMOTE_USER VB_JUMP_HOST VB_JUMP_USER VB_REMOTE_PORT VB_LOCAL_PORT VB_CADENCE_CSHRC VB_USE_SSH_CONFIG_JUMP; do
    profiled="${key}_${BRIDGE_PROFILE}"
    if [[ ${!profiled+x} ]]; then
      export "$key=${!profiled}"
    fi
  done
}
apply_bridge_profile

: "${VB_REMOTE_PORT:=65081}"
: "${VB_LOCAL_PORT:=65082}"
: "${VB_SSH_CONNECT_TIMEOUT:=20}"
: "${VB_SSH_SERVER_ALIVE_INTERVAL:=10}"
: "${VB_SSH_SERVER_ALIVE_COUNT_MAX:=2}"
: "${VB_USE_SSH_CONFIG_JUMP:=0}"

if lsof -tiTCP:"$VB_LOCAL_PORT" -sTCP:LISTEN -n -P >/dev/null 2>&1; then
  echo "bridge tunnel already listening on localhost:$VB_LOCAL_PORT"
else
  : "${VB_REMOTE_HOST:?VB_REMOTE_HOST missing in $BRIDGE_ENV}"
  : "${VB_REMOTE_USER:?VB_REMOTE_USER missing in $BRIDGE_ENV}"
  SSH_ARGS=(
    -f
    -o BatchMode=yes
    -o StrictHostKeyChecking=no
    -o ExitOnForwardFailure=yes
    -o ConnectTimeout="${VB_SSH_CONNECT_TIMEOUT}"
    -o ServerAliveInterval="${VB_SSH_SERVER_ALIVE_INTERVAL}"
    -o ServerAliveCountMax="${VB_SSH_SERVER_ALIVE_COUNT_MAX}"
    -o LogLevel=ERROR
  )
  if [[ "$VB_USE_SSH_CONFIG_JUMP" == "1" ]]; then
    echo "using ssh_config ProxyJump route for ${VB_REMOTE_HOST}" >&2
  elif [[ -n "${VB_JUMP_HOST:-}" ]]; then
    JUMP_USER="${VB_JUMP_USER:-$VB_REMOTE_USER}"
    SSH_ARGS+=(-J "${JUMP_USER}@${VB_JUMP_HOST}")
  fi
  SSH_ARGS+=("${VB_REMOTE_USER}@${VB_REMOTE_HOST}" "-L" "${VB_LOCAL_PORT}:127.0.0.1:${VB_REMOTE_PORT}" "-N")
  if ! ssh "${SSH_ARGS[@]}"; then
    echo "failed to start bridge tunnel on localhost:$VB_LOCAL_PORT" >&2
    PREFLIGHT_ARGS=(--bridge-repo "$BRIDGE_REPO")
    if [[ -n "$BRIDGE_PROFILE" ]]; then
      PREFLIGHT_ARGS+=(--profile "$BRIDGE_PROFILE")
    fi
    python3 "$ROOT_DIR/runners/bridge_preflight.py" "${PREFLIGHT_ARGS[@]}" || true
    exit 1
  fi
  echo "started bridge tunnel on localhost:$VB_LOCAL_PORT -> ${VB_REMOTE_HOST}:${VB_REMOTE_PORT}"
fi

PREFLIGHT_ARGS=(--bridge-repo "$BRIDGE_REPO")
if [[ -n "$BRIDGE_PROFILE" ]]; then
  PREFLIGHT_ARGS+=(--profile "$BRIDGE_PROFILE")
fi
python3 "$ROOT_DIR/runners/bridge_preflight.py" "${PREFLIGHT_ARGS[@]}"

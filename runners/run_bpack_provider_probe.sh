#!/usr/bin/env bash
set -euo pipefail

# Small pre-flight probe for model/provider comparability on bpack-v1.
#
# Purpose:
#   1. Stress high-output/high-truncation tasks before any full benchmark run.
#   2. Fix a cross-model baseline for max_tokens, temperature, top_p, and workers.
#   3. Record provider reasoning settings and hidden reasoning tokens when exposed.
#
# Required:
#   Provider API env for MODEL, for example MIMO_API_KEY for mimo-v2.5-pro.
#
# Optional:
#   MODEL=mimo-v2.5-pro
#   BENCH_DIR=benchmark-bpack-v1
#   DATE_TAG=20260508
#   GEN_WORKERS=8
#   MAX_TOKENS=4096
#   PUBLIC_SPEC_MODE=spectre-strict-v3
#   TIMEOUT_S=240
#   PROBE_TASKS="task_a task_b ..."
#
# MiMo defaults:
#   MIMO_BASE_URL defaults to the token-plan CN endpoint used in this project.
#   MIMO_THINKING_TYPE defaults to disabled unless explicitly set by caller.

MODEL="${MODEL:-mimo-v2.5-pro}"
BENCH_DIR="${BENCH_DIR:-benchmark-bpack-v1}"
DATE_TAG="${DATE_TAG:-$(date +%Y%m%d)}"
GEN_WORKERS="${GEN_WORKERS:-8}"
MAX_TOKENS="${MAX_TOKENS:-4096}"
PUBLIC_SPEC_MODE="${PUBLIC_SPEC_MODE:-spectre-strict-v3}"
TIMEOUT_S="${TIMEOUT_S:-240}"

if [[ "$MODEL" == mimo* ]]; then
  if [[ -z "${MIMO_API_KEY:-}" ]]; then
    echo "[bpack-provider-probe] ERROR: MIMO_API_KEY is not set." >&2
    exit 1
  fi
  export MIMO_BASE_URL="${MIMO_BASE_URL:-https://token-plan-cn.xiaomimimo.com/v1}"
  export MIMO_THINKING_TYPE="${MIMO_THINKING_TYPE:-disabled}"
fi

if [[ -n "${PROBE_TASKS:-}" ]]; then
  # shellcheck disable=SC2206
  TASKS=(${PROBE_TASKS})
else
  TASKS=(
    bpack_dwa_pointer_e2e
    bpack_flash_adc_3b_e2e
    bpack_prbs7_lfsr_e2e
    bpack_pulse_stretcher_e2e
    bpack_window_detector_e2e
    bpack_dwa_pointer_dut
    bpack_flash_adc_3b_bugfix
    bpack_dwa_pointer_tb
  )
fi

TASK_ARGS=()
for task in "${TASKS[@]}"; do
  TASK_ARGS+=(--task "$task")
done

SLUG="${MODEL//[^A-Za-z0-9_.-]/_}"
REASONING_LABEL="${REASONING_LABEL:-${MIMO_THINKING_TYPE:-provider-default}}"
GEN_DIR="generated-probe-bpack-${SLUG}-${PUBLIC_SPEC_MODE}-${REASONING_LABEL}-w${GEN_WORKERS}-${DATE_TAG}"
RESULT_DIR="results-probe-bpack-${SLUG}-${PUBLIC_SPEC_MODE}-${REASONING_LABEL}-w${GEN_WORKERS}-${DATE_TAG}"
SUMMARY_PREFIX="results/probe-bpack-${SLUG}-${PUBLIC_SPEC_MODE}-${REASONING_LABEL}-w${GEN_WORKERS}-${DATE_TAG}"

printf '[bpack-provider-probe] model=%s\n' "$MODEL"
printf '[bpack-provider-probe] bench=%s tasks=%s\n' "$BENCH_DIR" "${#TASKS[@]}"
printf '[bpack-provider-probe] public_spec_mode=%s max_tokens=%s workers=%s\n' "$PUBLIC_SPEC_MODE" "$MAX_TOKENS" "$GEN_WORKERS"
printf '[bpack-provider-probe] reasoning_label=%s\n' "$REASONING_LABEL"
printf '[bpack-provider-probe] generated=%s\n' "$GEN_DIR"
printf '[bpack-provider-probe] results=%s\n' "$RESULT_DIR"

python3 runners/generate.py \
  --model "$MODEL" \
  --bench-dir "$BENCH_DIR" \
  --output-dir "$GEN_DIR" \
  --public-spec-mode "$PUBLIC_SPEC_MODE" \
  --temperature 0 \
  --top-p 1 \
  --max-tokens "$MAX_TOKENS" \
  --max-workers "$GEN_WORKERS" \
  "${TASK_ARGS[@]}"

python3 runners/validate_benchmark_v2_gold.py \
  --backend evas \
  --bench-dir "$BENCH_DIR" \
  --family bpack-v1 \
  --candidate-dir "$GEN_DIR" \
  --model "$MODEL" \
  --output-dir "$RESULT_DIR" \
  --timeout-s "$TIMEOUT_S" \
  "${TASK_ARGS[@]}"

python3 runners/summarize_experiment_costs.py \
  --generated-dir "$GEN_DIR" \
  --bench-dir "$BENCH_DIR" \
  --result-dir "$RESULT_DIR" \
  --output-prefix "$SUMMARY_PREFIX"

export BPACK_PROBE_MODEL="$MODEL"
export BPACK_PROBE_BENCH_DIR="$BENCH_DIR"
export BPACK_PROBE_PUBLIC_SPEC_MODE="$PUBLIC_SPEC_MODE"
export BPACK_PROBE_MAX_TOKENS="$MAX_TOKENS"
export BPACK_PROBE_GEN_WORKERS="$GEN_WORKERS"
export BPACK_PROBE_TIMEOUT_S="$TIMEOUT_S"
export BPACK_PROBE_REASONING_LABEL="$REASONING_LABEL"
export BPACK_PROBE_TASKS="$(printf '%s\n' "${TASKS[@]}")"
export BPACK_PROBE_GEN_DIR="$GEN_DIR"
export BPACK_PROBE_RESULT_DIR="$RESULT_DIR"
export BPACK_PROBE_SUMMARY_PREFIX="$SUMMARY_PREFIX"
python3 - <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

config = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "model": os.environ["BPACK_PROBE_MODEL"],
    "bench_dir": os.environ["BPACK_PROBE_BENCH_DIR"],
    "public_spec_mode": os.environ["BPACK_PROBE_PUBLIC_SPEC_MODE"],
    "max_tokens": int(os.environ["BPACK_PROBE_MAX_TOKENS"]),
    "gen_workers": int(os.environ["BPACK_PROBE_GEN_WORKERS"]),
    "timeout_s": int(os.environ["BPACK_PROBE_TIMEOUT_S"]),
    "reasoning_label": os.environ["BPACK_PROBE_REASONING_LABEL"],
    "mimo_base_url": os.environ.get("MIMO_BASE_URL", ""),
    "mimo_thinking_type": os.environ.get("MIMO_THINKING_TYPE", ""),
    "mimo_reasoning_effort": os.environ.get("MIMO_REASONING_EFFORT", ""),
    "tasks": [line for line in os.environ["BPACK_PROBE_TASKS"].splitlines() if line],
    "generated_dir": os.environ["BPACK_PROBE_GEN_DIR"],
    "result_dir": os.environ["BPACK_PROBE_RESULT_DIR"],
    "summary_prefix": os.environ["BPACK_PROBE_SUMMARY_PREFIX"],
}
path = Path(os.environ["BPACK_PROBE_SUMMARY_PREFIX"] + ".config.json")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"[bpack-provider-probe] config={path}")
PY

printf '[bpack-provider-probe] summary=%s.md\n' "$SUMMARY_PREFIX"

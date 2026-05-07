# MiMo Full-Run Plan

This plan runs the unified `D` condition on `benchmark-balanced` with Xiaomi MiMo.

## Condition

- Benchmark: `benchmark-balanced` full 143 tasks.
- Model: `mimo-v2.5-pro`.
- Prompt condition: `D = spectre-strict-v3`, one-shot generation, no repair.
- Thinking mode: use `MIMO_THINKING_TYPE=disabled` for the controlled MiMo row.
  The provider-default row is diagnostic only because hidden reasoning can
  consume the visible output budget.
- Validator: spectre-strict EVAS through `runners/validate_benchmark_v2_gold.py --candidate-dir ... --bench-dir benchmark-balanced`.
- Accounting: `generation_meta.json` plus `summarize_experiment_costs.py` grouped tables. Record input tokens, output tokens, hidden reasoning tokens when reported, cached input tokens when reported, and API elapsed time.

## Command

Set `MIMO_API_KEY` in the shell, then run:

```bash
MIMO_API_KEY=... runners/run_mimo_d_full.sh
```

Optional knobs:

```bash
MODEL=mimo-v2.5-pro
MIMO_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
MIMO_THINKING_TYPE=disabled
GEN_WORKERS=8
MAX_TOKENS=4096
TIMEOUT_S=240
DATE_TAG=2026-05-04
```

Before a full run, execute the fixed high-output provider probe:

```bash
MIMO_API_KEY=... MODEL=mimo-v2.5-pro GEN_WORKERS=8 MAX_TOKENS=4096 \
  runners/run_bpack_provider_probe.sh
```

The 2026-05-08 probe result showed:

- `MIMO_REASONING_EFFORT=low` did not control hidden reasoning: a high-risk
  task still used about 4095 hidden reasoning tokens and produced no code.
- `MIMO_THINKING_TYPE=disabled` was accepted and set `reasoning_tokens=0`.
- `GEN_WORKERS=8` completed 8 parallel high-risk tasks without API errors.
- The controlled probe generated code for all 8 tasks; 1/8 still reached
  `max_tokens=4096` because visible output was long.

For any provider/model, the probe must confirm:

- `reasoning_tokens / output_tokens` is low or zero when the provider reports it.
- `raw_response_length > 0`.
- Required fenced code blocks are extracted.
- The selected setting appears in `generation_meta.json`.

## Expected Artifacts

- Generated root: `generated-balanced-D-strictv3-mimo-v2.5-pro-2026-05-04`
- Result root: `results/balanced-D-strictv3-mimo-v2.5-pro-spectre-strict-evas-2026-05-04`
- Cost summary: `results/mimo-D-strictv3-mimo-v2.5-pro-2026-05-04.md`

## Follow-Up Decision

After the full `D` row:

1. If compile failures dominate, run `C-SKILL` / `C-ULTRA` on MiMo-D candidates.
2. If compile is clean but behavior is weak, run public-only `G0` mechanism guidance.
3. Only run `F` or `I` after the D failure distribution is clear.

# MiMo Full-Run Plan

This plan runs the unified `D` condition on `benchmark-balanced` with Xiaomi MiMo.

## Condition

- Benchmark: `benchmark-balanced` full 143 tasks.
- Provider/model id: `provider=mimo`, `model_id=mimo-v2.5-pro`.
- Endpoint/profile: Xiaomi MiMo token-plan OpenAI-compatible endpoint.
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

- `provider=mimo`, `model_id=mimo-v2.5-pro`.
- `MIMO_REASONING_EFFORT=low` did not control hidden reasoning: a high-risk
  task still used about 4095 hidden reasoning tokens and produced no code.
- `MIMO_THINKING_TYPE=disabled` was accepted and set `reasoning_tokens=0`.
- `GEN_WORKERS=8` completed 8 parallel high-risk tasks without API errors.
- The controlled probe generated code for all 8 tasks; 1/8 still reached
  `max_tokens=4096` because visible output was long.

## Reasoning-Mode Ablation

A fixed 8-task high-output bpack probe was used to decide whether MiMo
reasoning should be enabled before any full benchmark row.

| Mode | Max tokens | Generated | No code | Length finishes | Hidden reasoning tokens | Avg API s/task | strict-EVAS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `MIMO_THINKING_TYPE=disabled` | 4096 | 8/8 | 0/8 | 1/8 | 0 | 21.2 | 1/8 |
| provider default | 4096 | 1/8 | 7/8 | 7/8 | 29,534 | 63.5 | 0/8 |
| provider default | 8192 | 3/8 | 5/8 | 5/8 | 57,582 | 117.2 | 1/8 |

Conclusion: provider-default reasoning fails the artifact gate for this
code-generation workload. Increasing the output budget to 8192 reduces but does
not solve `no_code_extracted`, and it costs about 5.5x the controlled
`thinking=disabled` average API time on the probe.  The mainline MiMo mode is
therefore `MIMO_THINKING_TYPE=disabled`, `MAX_TOKENS=4096`, and
`GEN_WORKERS=8`.  Provider-default reasoning rows are diagnostic only unless a
future prompt/model configuration passes the same artifact gate.

For any provider/model, the probe must confirm:

- The exact provider/model id is present in `generation_meta.json` and tables.
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

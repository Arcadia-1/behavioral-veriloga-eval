# bpack48 Priority Experiment Queue

**Date**: 2026-05-08

This queue narrows `bpack48` experiments to priority 1 and priority 2 only.
`evas-repair`, `mechanism-public`, and `functional-ir` are explicitly excluded
from the first bpack run cycle.

## Prerequisites

| Step | Output | Status |
| --- | --- | --- |
| B0 inventory | `docs/BPACK_V1_INVENTORY.json` | drafted |
| B1 benchmark root | `benchmark-bpack-v1/` | frozen bpack48: 48/48 tasks |
| B2 gold validation | EVAS+Spectre gold validation summary | strict-EVAS 48/48; Spectre 48/48 |
| Provider availability | Valid model API key in environment | MiMo key available for smoke/model runs |

Model experiments can start because B1 and B2 pass.

Current draft status is summarized in
`docs/BPACK_V1_MATERIALIZATION_REPORT.md` and
`docs/BPACK_V1_FREEZE_CANDIDATE_REPORT.md`.  The benchmark is runnable,
task-form complete, and gold-validated by both strict-EVAS and Spectre.

## Priority 1: Minimal Main Chain

Run these first:

| Order | Condition | Purpose | Depends on |
| --- | --- | --- | --- |
| P1.1 | `prompt-only` | Lower baseline on balanced packs. | B2 gold validation |
| P1.2 | `rules-only` | Strong public-rule baseline. | P1.1 optional, B2 required |
| P1.3 | `compile-loop` | LLM compile-first closure. | `rules-only` artifacts/results |
| P1.4 | `compile-skill-advanced` | Current best compile-skill stack. | `compile-loop` artifacts/results |

Primary questions:

1. Does `rules-only` still dominate `prompt-only` when task forms are balanced?
2. Does `compile-loop` still improve compile closure?
3. Does the best compile-skill stack still improve pack-level pass metrics?

## Priority 2: Compile-Skill Ablation Detail

Run only after P1 shows that `compile-skill-advanced` improves over
`compile-loop`.

| Order | Condition | Purpose | Depends on |
| --- | --- | --- | --- |
| P2.1 | `compile-skill-prompt` | Isolate prompt-side compile skill guidance. | `compile-loop` artifacts/results |
| P2.2 | `compile-skill-accept` | Isolate accept/reject local skill layer. | `compile-loop` artifacts/results |

## Excluded From This Cycle

| Condition | Reason |
| --- | --- |
| `evas-repair` | Generic repair negative control; appendix only after main chain stabilizes. |
| `mechanism-public` | Behavior mechanism hypothesis; wait for bpack residual taxonomy. |
| `functional-ir` | IR hypothesis; wait for bpack residual taxonomy. |

## Reporting For Every Run

Report both task-level and pack-level metrics:

| Metric | Required |
| --- | --- |
| `PASS/48` | yes |
| `Pack success` | yes |
| `Avg forms/pass per pack` | yes |
| Pass by task form | yes |
| Compile pass rate | yes |
| Sim correctness rate | yes |
| Avg tokens/task | yes |
| Avg API time/task | yes |
| Exact provider | yes |
| Exact model id | yes |
| Model thinking/reasoning mode | yes |

## Provider Probe Before Full Runs

Before running a new model/provider on the full bpack benchmark, run the fixed
high-output probe:

```bash
MODEL=<model> GEN_WORKERS=8 MAX_TOKENS=4096 runners/run_bpack_provider_probe.sh
```

The current MiMo controlled setting is:

- `provider=mimo`
- `MODEL=mimo-v2.5-pro`
- `MIMO_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1`
- `MIMO_THINKING_TYPE=disabled`
- `MAX_TOKENS=4096`
- `GEN_WORKERS=8`
- `temperature=0`, `top_p=1`

The 2026-05-08 MiMo probe passed the provider gate:

- 8/8 high-output tasks generated extractable code.
- 0 API errors at `GEN_WORKERS=8`.
- 0 hidden reasoning tokens with `MIMO_THINKING_TYPE=disabled`.
- 1/8 tasks still hit `finish_reason=length`, now due to visible output length
  rather than hidden reasoning.

The Kimi reference rows should be reported as:

- `provider=bailian` / Bailian-Anthropic-compatible route
- `model_id=kimi-k2.5`
- `reasoning_mode=provider-default/not-reported`

Do not report broad model-family labels such as only `Kimi` or only `MiMo` in
tables; use the exact provider/model id pair.

## Stop/Go Gates

| Gate | Decision |
| --- | --- |
| Gold validation fails | Do not run models; fix benchmark. |
| `rules-only` fails to generate usable artifacts | Fix prompt/provider extraction before P1.3. |
| `compile-loop` increases compile failures | Debug closure loop before skill rows. |
| `compile-skill-advanced` does not improve P1 metrics | Run P2 ablations to locate regression before any behavior experiments. |

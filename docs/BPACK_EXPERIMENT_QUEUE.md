# bpack48 Priority Experiment Queue

**Date**: 2026-05-07

This queue narrows `bpack48` experiments to priority 1 and priority 2 only.
`evas-repair`, `mechanism-public`, and `functional-ir` are explicitly excluded
from the first bpack run cycle.

## Prerequisites

| Step | Output | Status |
| --- | --- | --- |
| B0 inventory | `docs/BPACK_V1_INVENTORY.json` | drafted |
| B1 benchmark root | `benchmark-bpack-v1/` | TODO |
| B2 gold validation | EVAS+Spectre gold validation summary | TODO |
| Provider availability | Valid model API key in environment | blocked locally |

Model experiments must not start until B1 and B2 pass.

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
| Model thinking/reasoning mode | yes |

## Stop/Go Gates

| Gate | Decision |
| --- | --- |
| Gold validation fails | Do not run models; fix benchmark. |
| `rules-only` fails to generate usable artifacts | Fix prompt/provider extraction before P1.3. |
| `compile-loop` increases compile failures | Debug closure loop before skill rows. |
| `compile-skill-advanced` does not improve P1 metrics | Run P2 ablations to locate regression before any behavior experiments. |

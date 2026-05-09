# vaEVAS Mainline Protocol

**Date**: 2026-05-08

This document freezes the current vaEVAS research spine after the benchmark and
strategy confidence audit.  It is intentionally stricter than the historical
ADFGI/C-PLUS/ULTRA vocabulary: old names remain traceable, but new claims should
use the canonical benchmark, validator, and condition names below.

## Project Thesis

vaEVAS studies public-specification Verilog-A behavioral generation under a
Spectre-aligned validation loop.  The central question is:

```text
Given only a public behavioral circuit specification, can a model or repair
system generate Spectre-compatible Verilog-A that passes functional validation,
while controlling token/time cost?
```

Gold solutions are feasibility proofs and checker-validation anchors.  They are
not prompt-only baselines.  Codex/GPT-5.5 xhigh construction is an agentic upper
bound unless it is rerun under the same public-input, no-tool, fixed-budget
condition as other models.

## Benchmark Layers

| Layer | Canonical name | Role | Claim status |
| --- | --- | --- | --- |
| Development | `vaBench-dev48` / `benchmark-bpack-v1` / `bpack48` | Fast iteration, provider probes, runner validation, compile-skill/controller smokes. | Internal/dev evidence; not sufficient alone for final paper claims. |
| Main | `vaBench-main` | Larger balanced benchmark for main tables. | Must be built/frozen before final claims. |
| Heldout | `vaBench-heldout` | Family-level generalization and overfitting guard. | Required before claiming skill/RAG/controller generalization. |
| Stress | `vaBench-stress` | EVAS/Spectre edge cases such as sources, file IO, events, unsupported frontend forms. | Evaluator robustness evidence, not main generation score. |

Current `bpack48` readiness audit:

| Item | Status |
| --- | --- |
| Tasks | 48 |
| Concrete function packs | 12 |
| Task forms | 12 bugfix, 12 spec-to-va, 12 end-to-end, 12 tb-generation |
| Required files | 48/48 have `prompt.md`, `checker.py`, `checks.yaml`, `meta.json`, and gold files |
| Gold strict-EVAS | 48/48 per `docs/BPACK_V1_FREEZE_CANDIDATE_REPORT.md` |
| Gold Spectre | 48/48 per `docs/BPACK_V1_FREEZE_CANDIDATE_REPORT.md` |
| Audit artifact | `analysis/bpack48_benchmark_readiness_audit_20260508.json` |
| Semantic contract audit | 0 hard FAIL after DWA public save/column cleanup; remaining WARN are P1 prompt-cleanup items |

Decision: keep `bpack48` as the clean development set, then scale to
`vaBench-main` and `vaBench-heldout` before paper-facing generalization claims.

## Main Benchmark Construction Rule

The unit of benchmark expansion is a concrete circuit-function pack, not source
provenance such as `92+35+16`.

Each promoted pack should define:

| Field | Requirement |
| --- | --- |
| `circuit_function_id` | Stable concrete function, e.g. `hysteresis_comparator`, not a broad bucket. |
| `core_function` | Broader analysis group. |
| Task forms | Prefer all four canonical forms: `bugfix`, `spec-to-va`, `end-to-end`, `tb-generation`. |
| Public contract | Checker-observed behavior must be stated in `prompt.md`. |
| Gold | Gold artifacts pass strict-EVAS and Spectre before model runs. |
| Duplicate policy | Do not add another task with the same function, form, and observable behavior. |
| Leakage policy | No task-id, gold, hidden checker logic, or directory-name routing in model prompts, skill retrieval, RAG, or controller decisions. |

Recommended scale targets:

| Target | Size | Purpose |
| --- | ---: | --- |
| `vaBench-main-120` | 30 packs x 4 forms | Selected v1 main benchmark target. |
| `vaBench-main-192` | 48 packs x 4 forms | Deferred v2 expansion for stronger statistical stability. |
| `vaBench-heldout-48` | 12 unseen packs x 4 forms | Heldout family generalization. |
| `vaBench-stress` | variable | Evaluator/Spectre edge cases, separated from main score. |

The concrete v1 pack list is frozen in `docs/VABENCH_MAIN_COVERAGE_TABLE.md`.

## Canonical Validators

| Validator | Role | Claim boundary |
| --- | --- | --- |
| `strict-evas` | Fast main evaluator: Spectre-compatible preflight, EVAS simulation, checker. | Used for full-run iteration and main internal scoring. |
| `spectre-audit` | Real Spectre execution plus the same checker. | Final judge for paper-facing pass claims and parity slices. |
| `both-audit` | Paired strict-EVAS and Spectre on the same artifacts. | Required for parity evidence and high-impact deltas. |

`strict-evas` is one evaluator with internal layers: frontend preflight rejects
Spectre-incompatible source before simulation, and parser/kernel parity fixes make
EVAS behavior match Spectre on legal inputs.  These layers are separated because
some failures are illegal source issues and others are simulator semantics issues.

## Validation Run Policy

Default development validation is targeted regression plus result splicing, not
full rerun.

| Stage | Action | Purpose |
| --- | --- | --- |
| Targeted regression | Rerun only tasks affected by the changed mechanism. | Fast proof that the patch fixes intended cases and does not break nearby cases. |
| Result splice | Replace affected task results in the previous full root and recompute summary. | Estimate updated full-table metrics without rerunning unaffected tasks. |
| Checkpoint full | Rerun full EVAS/Spectre only at claim or merge boundaries. | Confirm no hidden global regression before paper/PR claims. |

Use `runners/splice_validation_results.py` for the splice step.  The script
records a `splice_manifest.json`, recomputes `summary.json`, and can compare the
spliced root against Spectre or a checkpoint full root.

Use `runners/tag_benchmark_features.py` and `runners/select_affected_tasks.py`
to avoid hand-picking targeted sets:

```bash
python3 runners/tag_benchmark_features.py \
  --bench-dir benchmark-vabench-main-v1 \
  --scope executable \
  --output analysis/vabench_main120_feature_tags_20260508.json

python3 runners/select_affected_tasks.py \
  --features-json analysis/vabench_main120_feature_tags_20260508.json \
  --change-type cross \
  --format args
```

Feature selection is a coverage guard, not a promise that every regression set
will be tiny.  Some mechanisms, such as `transition` and PWL sources, are common
across Main120.  In those cases, run a smoke subset with `--form`, `--pack`, or
`--max-tasks`, then use checkpoint full only when the splice delta matters.

Splice is a development estimator, not a substitute for a checkpoint full run.
It is valid for changed-task accounting when the affected set is explicit and
the unchanged task artifacts are reused byte-for-byte.  If the change touches a
global EVAS scheduler/kernel path, validator status mapping, checker semantics,
or source materialization shared by many tasks, run a targeted regression first
and schedule a checkpoint full before making a claim.

For candidate-specific regressions, include the generated root when tagging:

```bash
python3 runners/tag_benchmark_features.py \
  --bench-dir benchmark-vabench-main-v1 \
  --candidate-dir generated-main120-D-rulesonly-mimo-v2.5-pro-20260508-main120-D \
  --model mimo-v2.5-pro \
  --scope executable \
  --output analysis/main120_D_candidate_feature_tags_20260508.json
```

Pass selected tasks through a task file rather than shell-expanded `--task`
arguments when possible:

```bash
python3 runners/select_affected_tasks.py \
  --features-json analysis/main120_D_candidate_feature_tags_20260508.json \
  --change-type fileio \
  --format plain > analysis/affected_tasks_fileio_20260508.txt

PYTHONPATH=runners python3 runners/validate_benchmark_v2_gold.py \
  --backend evas \
  --bench-dir benchmark-vabench-main-v1 \
  --task-file analysis/affected_tasks_fileio_20260508.txt \
  ...
```

Use `runners/audit_failure_label_mismatches.py` when EVAS/Spectre PASS/FAIL
already agrees but the failure labels differ.  It keeps binary parity separate
from taxonomy cleanup.

Example:

```bash
python3 runners/splice_validation_results.py \
  --base-results results/main120-D-rulesonly-mimo-v2.5-pro-strict-evas-v2preflight-20260508-main120-D \
  --patch-results results/main120-D-targeted-parityfix-evas-20260508 \
  --output-results results/main120-D-spliced-parityfix-vs-spectre-20260508 \
  --backend evas \
  --family vabench-main-v1-main120-D-spliced-parityfix \
  --compare-results results/main120-D-rulesonly-mimo-v2.5-pro-spectre-jin-20260508-main120-D \
  --force
```

Current sanity check: replacing only five targeted EVAS parity tasks in the old
D full root reproduces the full parityfix checkpoint exactly: 21/120 PASS and
0/120 status mismatches versus the checkpoint full EVAS root.  Against Spectre,
the spliced root has 0/120 binary PASS/FAIL mismatches and 12 failure-label-only
mismatches.

Selector-driven smoke practice:

- Selector: `--change-type fileio`.
- Selected tasks: 4 `file_metric_writer` tasks.
- Targeted run: `results/main120-D-targeted-fileio-selector-smoke-evas-20260508`, EVAS 0/4.
- Spliced output: `results/main120-D-spliced-fileio-selector-smoke-20260508`, EVAS 21/120.
- Checkpoint comparison: 0 binary and 0 status mismatches versus full EVAS parityfix checkpoint.
- Spectre comparison: 0 binary PASS/FAIL mismatches and the same 12 failure-label-only mismatches.

2026-05-09 red-team loop:

- Rebuilt tags with `--scope executable` and candidate-aware scanning.
- Added uncertainty markers for macro/include patterns; current D candidate tags report 12 `has_macro_use` tasks.
- Added `--include-uncertain` selector mode; `fileio` expands from 4 direct tasks to 16 conservative tasks when uncertainty is included.
- Ran an event/parity targeted regression selected by `cross + pulse + abstime` over the four recently repaired packs: `barrel_pointer_window`, `leaky_hold`, `sar_logic_4b`, and `track_hold_aperture`.
- Targeted output: `results/main120-D-targeted-event-parity-packs-evas-20260509`, EVAS 5/16.
- Spliced output: `results/main120-D-spliced-event-parity-packs-20260509`, EVAS 21/120.
- Checkpoint comparison: 0 binary and 0 status mismatches versus full EVAS parityfix checkpoint.
- Spectre comparison: 0 binary PASS/FAIL mismatches and the same 12 failure-label-only mismatches.

Red-team fixes applied to the targeted/splice workflow:

| Risk | Fix |
| --- | --- |
| Feature tags polluted by prompt/checker text. | `tag_benchmark_features.py` defaults to `--scope executable`, scanning only `.va/.scs`; `--scope all` is explicit. |
| Candidate code can contain features absent from gold. | `tag_benchmark_features.py` supports `--candidate-dir`, `--model`, and `--sample-idx`. |
| Shell expansion of repeated `--task` is fragile in zsh. | `validate_benchmark_v2_gold.py` supports `--task-file`; selector can emit plain task lists. |
| Empty or misspelled affected selections can silently skip validation. | `select_affected_tasks.py` now exits nonzero unless `--allow-empty` is set. |
| `--max-tasks` can accidentally drop forced tasks. | Forced tasks are sorted first before truncation. |

Current Main120 feature-tag artifact:

```text
analysis/vabench_main120_feature_tags_20260508.json
```

Current D EVAS/Spectre label audit:

```text
analysis/main120_d_evas_spectre_failure_label_mismatch_normalized_20260509.json
analysis/main120_d_evas_spectre_failure_label_mismatch_normalized_20260509.csv
```

Failure-label taxonomy normalization:

- Raw backend `status` is never rewritten.
- Analysis uses `normalized_status` for binary PASS/FAIL, plus `failure_stage`, `failure_origin`, and `failure_reason`.
- Normalization reads backend diagnostics such as `spectre_errors`; raw `notes` alone can hide the concrete Spectre failure reason behind `returncode=2`.
- Pair-level EVAS/Spectre comparison is canonical for label-only mismatch analysis because one backend may expose a more specific failure signature than the other.
- Current Main120 D parityfix audit: 12 raw status-label mismatches, 0 binary PASS/FAIL mismatches.
- Pair-level reason buckets: `unsupported_or_nonstandard_symbol` 6, `tb_source_or_netlist_parse` 4, `conditional_transition_semantics` 1, `interface_source_drive` 1.

EVAS reporting is part of the simulator objective, not just table cleanup.
When EVAS exposes a Spectre-style source failure during runtime, it should emit
structured diagnostics and align the compile/behavior axes accordingly.  Current
diagnostic refinement covers unsupported/nonstandard time symbols, conditional
`transition()`, malformed source/PWL parsing, and interface source-drive errors.
The targeted diagnostic splice keeps D at 21/120 PASS and 0/120 binary
EVAS/Spectre mismatch, while reducing raw status-label mismatches from 12 to 6.

Current taxonomy artifacts:

```text
analysis/main120_d_evas_normalized_failure_taxonomy_20260509.json
analysis/main120_d_evas_normalized_failure_taxonomy_20260509.csv
analysis/main120_d_spectre_normalized_failure_taxonomy_20260509.json
analysis/main120_d_spectre_normalized_failure_taxonomy_20260509.csv
```

## Canonical Conditions

| ID | Canonical condition | Adds what | Main role |
| --- | --- | --- | --- |
| A | `prompt-only` | Public prompt only, one generation, no rule pack, no repair. | Bare model capability. |
| D | `rules-only` | Public Verilog-A/Spectre rules in the prompt, one generation. | Rule baseline. |
| C | `compile-loop` | D plus EVAS compile/preflight feedback repair loop. | Feedback-loop baseline. |
| S1 | `compile-skill-prompt` | Compile skills inserted as public prompt guidance. | Context-engineering compile skill contribution. |
| S2 | `compile-skill-accept` | Local/public compile skills propose candidates; strict-EVAS accept/reject decides. | Deterministic skill contribution and cost control. |
| B | `behavior-skill` | Behavior/mechanism repair only after compile closure. | Next-stage behavior correctness branch. |
| T | `tool-controller` | Routes among local skills, LLM repair, behavior tools, RAG, Spectre audit, or stop. | Efficiency and composition. |
| R | `repair-trace-rag` | Retrieves high-quality accepted/rejected repair traces. | Experience transfer, after trace dataset is clean. |
| O | `agentic-upper-bound` | Codex/GPT-5.5 xhigh or human/agent gold construction. | Feasibility/upper-bound only, not a fair baseline. |

Retire from main tables: `C-PLUS`, `C-SKILLPLUS`, `C-ULTRA`,
`C-ULTRA-ADVANCED`, `G0`, and legacy ADFGI names.  They may appear only in
legacy-to-canonical notes.

## Required Metrics

Every reported row must include:

| Metric | Why |
| --- | --- |
| `PASS/N` under `strict-evas` | Primary fast score. |
| Spectre pass or audit scope | Final trust anchor. |
| Compile/interface failures | Separates legality from behavior. |
| Behavior failures | Shows whether compile closure actually improves correctness. |
| PASS by task form | Prevents end-to-end or bugfix dominance. |
| PASS by circuit pack/family | Detects overfitting to one mechanism. |
| Pack success and average forms/pass per pack | Main reason to use function packs. |
| Input/output/reasoning/total tokens | Cost accounting. |
| API time and local eval time | Latency and controller efficiency. |
| Model/provider/reasoning settings | Cross-model fairness. |

## Model Setting Parity

Before any full model row, run a provider smoke/probe.  Freeze:

| Setting | Requirement |
| --- | --- |
| exact provider and model id | No broad family labels alone. |
| `temperature`, `top_p` | Fixed per benchmark row. |
| `max_tokens` | Matched unless provider limit forces an explicit exception. |
| reasoning/thinking mode | Explicitly reported and smoke-tested. |
| worker count and timeout | Fixed and reported. |
| code extraction and truncation | Smoke must show low/no systematic failure before full run. |

MiMo-specific current controlled mode is `mimo-v2.5-pro` with thinking disabled;
provider-default reasoning is diagnostic until it passes the same artifact gate.

## Confidence Audit Loop

Current high-confidence strategy after red-team review:

| Risk | Fix | Status |
| --- | --- | --- |
| `bpack48` is too small for final claims. | Use it only as dev set; build `vaBench-main` and `vaBench-heldout`. | Fixed in protocol. |
| Prompt/checker mismatch can make failures unfair. | Add prompt-checker-gold audit before benchmark freeze. | Required gate. |
| Gold from Codex/GPT-5.5 xhigh can be mistaken for a fair baseline. | Label as `agentic-upper-bound`; rerun under A if used as a model baseline. | Fixed in protocol. |
| EVAS/Spectre mismatch can invalidate repair conclusions. | Use `both-audit` on gold, high-impact deltas, and representative residual slices. | Required gate. |
| Compile skills can overfit to benchmark artifacts. | Only public-trigger, rule/generalizable skills; heldout promotion required. | Required gate. |
| Too many condition names obscure the story. | Canonical A/D/C/S1/S2/B/T/R/O only. | Fixed in protocol. |
| PASS-only reporting hides cost and failure shifts. | Require pass, failure family, tokens, API time, local eval time. | Fixed in protocol. |
| Early SFT/RL can fit noise. | Delay until trace schema, main benchmark, and heldout are stable. | Fixed in protocol. |

No strategy is literally 100% certain.  This protocol reaches practical high
confidence because each major remaining failure mode has a concrete gate before
it can become a paper claim.

## Execution Order

1. Freeze this protocol and update pointers from old docs.
2. Keep `bpack48` as dev set; do not make final claims from it alone.
3. Run prompt-checker-gold audit on any benchmark before model evaluation.
4. Design `vaBench-main` pack coverage and split out `vaBench-heldout` by circuit-function family.
5. Run A/D/C/S1/S2 on dev set only to validate infrastructure.
6. Run A/D/C/S1/S2 on `vaBench-main` for primary tables.
7. Build failure taxonomy from main residuals.
8. Add B only on compile-passing behavior residuals.
9. Add T after useful tools exist and compare cost-pass Pareto.
10. Accumulate repair traces, then test R; only then consider SFT/DPO/RL.

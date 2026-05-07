# Balanced Function-Pack Benchmark Plan

**Date**: 2026-05-07

This document plans the cleaner balanced benchmark that should sit next to the
current `b143` benchmark.  It does not replace `b143` immediately.  It defines a
new benchmark family whose unit is a concrete circuit function pack.

## Motivation

`b143` is useful as the current maintained mainline benchmark, but it is not an
exact four-form balanced benchmark.  It is task-form covered across broad
`core_function` labels, while some labels contain many different concrete
circuits and the task-form counts are uneven:

| Task form | Count in `b143` |
| --- | ---: |
| `bugfix` | 25 |
| `spec-to-va` | 33 |
| `end-to-end` | 62 |
| `tb-generation` | 23 |

The cleaner benchmark should answer a different question:

```text
For the same concrete circuit function, how does the model perform across
bugfix, spec-to-va, end-to-end, and testbench-generation forms?
```

## Benchmark Name

Use a new benchmark name rather than mutating `b143`:

| Name | Meaning |
| --- | --- |
| `bpack-v1` | Exact circuit-function pack benchmark, version 1. |
| `bpack48` | Suggested first size: 12 concrete circuit functions x 4 task forms. |
| `bpack88` | Larger option: 22 concrete circuit functions x 4 task forms. |

Recommended start: `bpack48`.  It is large enough to cover circuit diversity but
small enough to validate with full EVAS and broad Spectre audit.

## Unit Of Balance

The balancing unit is `circuit_function_id`, not broad `core_function`.

Example:

| Broad label | Concrete `circuit_function_id` examples |
| --- | --- |
| `digital-logic` | `not_gate`, `gray_counter`, `serializer`, `clock_divider` |
| `comparator` | `hysteresis_comparator`, `strongarm_comparator`, `offset_comparator` |
| `data-converter` | `flash_adc_3b`, `binary_dac_4b`, `thermometer_dac`, `sar_adc_dac` |
| `pll-clock` | `adpll_timer`, `cppll_timer`, `multimod_divider` |

Each `circuit_function_id` contributes exactly four tasks:

1. `bugfix`
2. `spec-to-va`
3. `end-to-end`
4. `tb-generation`

## Task Contract

Each pack must share one public functional contract:

| Field | Requirement |
| --- | --- |
| `circuit_function_id` | Stable concrete function name. |
| `core_function` | Broader grouping for analysis. |
| `task_form` | One of the four canonical forms. |
| Public interface | Same conceptual ports/observables across forms when feasible. |
| Observable behavior | Same function-level behavior, but different task-form burden. |
| Gold validation | Gold artifacts pass `strict-evas`; representative/full pack passes `spectre-audit`. |
| Duplicate policy | Do not add another task with the same function, form, and observable behavior. |

## Seed Packs

The current exact four-form packs can seed `bpack-v1`:

| Pack | Status |
| --- | --- |
| `threshold_detector` | Exists in `b143`; four forms validated. |
| `window_detector` | Exists in `b143`; four forms validated. |
| `analog_limiter` | Exists in `b143`; four forms validated. |
| `pulse_stretcher` | Exists in `b143`; four forms validated. |

Recommended additional packs for `bpack48`:

| Candidate `circuit_function_id` | Broad group | Why include |
| --- | --- | --- |
| `sample_hold` | sample-hold | Classic analog memory behavior and aperture/droop checks. |
| `hysteresis_comparator` | comparator | Threshold and stateful hysteresis behavior. |
| `pfd_updn` | phase-detector | Event ordering, mutual exclusion, pulse behavior. |
| `clock_divider` | digital-logic / pll-clock | Sequential digital cadence and edge counting. |
| `binary_dac_4b` | data-converter | Static code-to-voltage mapping. |
| `flash_adc_3b` | data-converter | Threshold quantization and code coverage. |
| `dwa_pointer` | calibration / data-converter | Rotating pointer/window state behavior. |
| `prbs7_lfsr` | digital sequence | Stateful pseudo-random sequence behavior. |

This gives 12 packs x 4 forms = 48 tasks.

## Why Not Start With `bpack88`?

`bpack88` is attractive, but it requires 22 clean concrete function definitions
and 88 gold/checker/testbench contracts.  That is likely too much churn before
we finish the current vaEVAS paper spine.

Recommended path:

```text
bpack48 first -> validate methodology -> optionally scale to bpack88
```

## Construction Plan

### Stage B0: Pack Inventory

Audit candidate functions from `b143`, `benchmark-v2`, and existing gold tasks.
For each candidate, decide whether the function is concrete enough to become a
pack.

Output:

```text
docs/BPACK_V1_INVENTORY.json
```

Required fields:

```json
{
  "circuit_function_id": "sample_hold",
  "core_function": "sample-hold",
  "forms": {
    "bugfix": "existing_or_new_task_id",
    "spec-to-va": "existing_or_new_task_id",
    "end-to-end": "existing_or_new_task_id",
    "tb-generation": "existing_or_new_task_id"
  },
  "status": "existing|needs_authoring|needs_checker|needs_spectre_audit"
}
```

### Stage B1: Materialize `bpack48`

Create a separate benchmark root:

```text
benchmark-bpack-v1/
```

Do not mutate `benchmark-balanced/`.

Each task should contain:

```text
prompt.md
meta.json
checks.yaml
checker.py
gold/dut.va
gold/tb_ref.scs
```

Metadata should include:

```json
{
  "benchmark": "bpack-v1",
  "circuit_function_id": "sample_hold",
  "core_function": "sample-hold",
  "task_form": "spec-to-va",
  "pack_id": "sample_hold",
  "pack_version": "v1"
}
```

### Stage B2: Gold Validation

Run gold validation before any model run:

```bash
python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-bpack-v1 \
  --family bpack-v1 \
  --backend both \
  --output-dir results-bpack48__gold__both-audit__gold-validation__YYYYMMDD \
  --timeout-s 180
```

Promotion gate:

| Gate | Requirement |
| --- | --- |
| EVAS gold | 48/48 pass. |
| Spectre gold | 48/48 pass or documented exclusion before benchmark freeze. |
| Checker stability | No known timeout/flaky checker in gold. |
| Metadata | Every task has `circuit_function_id`, `core_function`, and canonical `task_form`. |

### Stage B3: Model Baselines

Use the clean condition names.  First full run set:

| Condition | Why run | Required? |
| --- | --- | --- |
| `prompt-only` | Lower baseline. | Yes |
| `rules-only` | Strong public-rule baseline. | Yes |
| `compile-loop` | LLM compile-first closure. | Yes |
| `compile-skill-prompt` | Prompt-side compile-skill contribution. | Yes |
| `compile-skill-accept` | Conservative skill accept/reject contribution. | Yes |
| `compile-skill-advanced` | Current best compile-skill stack. | Yes |
| `evas-repair` | Generic repair negative control. | Optional appendix |
| `mechanism-public` | Behavior mechanism hypothesis. | After residual taxonomy |
| `functional-ir` | IR hypothesis. | After residual taxonomy |

### Stage B4: Reporting

Primary table should report both full score and pack-balanced views:

| Column | Meaning |
| --- | --- |
| `PASS/48` | Main benchmark pass count. |
| `Pack success` | Number of packs where all four forms pass. |
| `Avg forms/pass per pack` | Mean pass count over four forms. |
| `Form pass rate` | Pass by bugfix/spec-to-va/end-to-end/tb-generation. |
| `Compile pass rate` | DUT/TB compile closure. |
| `Sim correctness` | Behavior correctness after compile. |
| `Avg tokens/task` | Cost. |
| `Avg API time/task` | Latency. |

Pack-level metrics are the main reason to build this benchmark.  They let us see
whether a method helps one form only or generalizes across a circuit function.

## Experiment Plan On `bpack48`

### Claim P1: Rules establish a strong baseline

Compare:

```text
prompt-only -> rules-only
```

Success criterion: `rules-only` substantially improves compile and pass rate
without Spectre audit mismatch.

### Claim P2: Compile skills improve legal executability across forms

Compare:

```text
rules-only -> compile-loop -> compile-skill-prompt -> compile-skill-accept -> compile-skill-advanced
```

Success criterion: compile failures decrease monotonically or nearly
monotonically, and pack-level pass metrics improve.

### Claim P3: Generic EVAS repair is not enough

Optional appendix comparison:

```text
rules-only -> evas-repair
```

Success criterion: if weak, it supports the current conclusion that skillized
compile closure is more useful than generic repair loops.

### Claim P4: Behavior mechanisms are a next-stage hypothesis

Do not run full `mechanism-public` until residual taxonomy shows behavior
failures that mechanism cards plausibly address.

## Run Order

| Step | Run | Gate |
| --- | --- | --- |
| 1 | Build inventory for 12 packs | Each pack has four concrete task contracts. |
| 2 | Materialize `benchmark-bpack-v1` | Metadata/schema check passes. |
| 3 | Gold EVAS+Spectre validation | 48/48 gold pass or benchmark not frozen. |
| 4 | `prompt-only` and `rules-only` | Extracted artifacts and token/time accounting valid. |
| 5 | `compile-loop` | Compile residuals measurable. |
| 6 | `compile-skill-prompt` | Prompt-side skill contribution measured. |
| 7 | `compile-skill-accept` / `compile-skill-advanced` | Best compile-skill stack measured. |
| 8 | Residual taxonomy | Decide whether `mechanism-public` or `functional-ir` is justified. |

## Relationship To `b143`

| Benchmark | Role |
| --- | --- |
| `b143` | Current broad-coverage maintained benchmark; preserves continuity with existing results. |
| `bpack48` | Cleaner balanced benchmark for pack-level method claims. |

Do not mix the two in one table without labels.  A result on `bpack48` should not
be presented as directly comparable to `b143` pass rates because the task mix is
different.

## Decision

Build `bpack48` as the next benchmark-cleanliness milestone.  Keep `b143` for
existing mainline continuity, but use `bpack48` to support cleaner benchmark and
pack-level method claims.

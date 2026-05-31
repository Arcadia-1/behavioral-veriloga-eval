# vaEVAS Validation Pipeline

Date: 2026-05-13

## Purpose

This document defines the validation gates for benchmark promotion and EVAS
parity work. The core rule is simple: benchmark claims need executable evidence,
and Spectre remains the final paper-facing judge.

## Reference And Equivalence Policy

EVAS validation targets Spectre-equivalent behavioral results, not
higher-than-Spectre analog precision. The benchmark-supported subset is pure
voltage-domain, event-driven Verilog-A; for this scope, the relevant standard is
whether EVAS preserves task-level behavior and stays within the same practical
waveform tolerance envelope as official Spectre runs.

Use Spectre modes as follows:

- `spectre/classic` is the conservative non-X reference path for gold
  promotion and disputed waveform behavior.
- `spectre/ax` is the fast official Spectre baseline for speed comparisons.
- AX/classic waveform differences are expected on event-driven behavioral
  tasks. Treat their self-consistency as the tolerance anchor; do not require
  EVAS to be more precise than both Spectre modes.

For the 2026-05-22 clean-repeat speed slice, this anchor is materialized in
`speed-optimization/reports/spectre_ax_classic_self_consistency_clean_repeats_20260522.json`.
It compares Spectre AX and Spectre classic directly on the same 1036 row pairs.

The current waveform gate in `run_gold_dual_suite.py` is therefore an
equivalence acceptance gate: behavior check first, then waveform parity within
the accepted tolerance. A pass means "Spectre-equivalent for the benchmark
contract", not "numerically more accurate than Spectre".

Report equivalence with simulator-style checks rather than percentile shorthand:

| Check | Role |
| --- | --- |
| Behavior/spec pass | Primary correctness signal; task checkers decide code, lock, edge count, gain, delay, and other observable contracts. |
| Event consistency | Discrete event order, edge count, and digital/rail-like mismatch must stay compatible with Spectre. |
| Relative RMS waveform error | Scale-normalized waveform difference, analogous to a reltol-style comparison. |
| Absolute voltage error | Near-zero or low-swing safeguard, analogous to an abstol-style comparison. |
| Reference self-consistency | AX/classic agreement defines the practical envelope for speed-mode comparisons. |

Implementation note: the current waveform gate in `run_gold_dual_suite.py` uses
row-mean relative RMS error plus worst-signal relative RMS error as the relative
condition, and max RMS voltage plus max point voltage as the absolute condition.
These constants are acceptance thresholds anchored by Spectre AX/classic
self-consistency, not a claim that EVAS has higher numeric precision than
Spectre.

## Track 1: Static Integrity

Use this before changing benchmark tasks, runners, or promotion docs.

```bash
python3 -m py_compile \
  runners/bridge_preflight.py \
  runners/run_gold_dual_suite.py \
  runners/gen_manifest.py \
  runners/gen_weekly_summary.py \
  runners/gen_paper_stats.py \
  runners/_result_table_utils.py

python3 -m pytest -q \
  tests/test_bridge_preflight.py \
  tests/test_bridge_scripts.py \
  tests/test_run_gold_dual_suite.py \
  tests/test_save_statements.py \
  tests/test_pwl_statements.py \
  tests/test_meta_schema.py
```

What this covers:

- `meta.json` schema validity.
- Required task files.
- Spectre testbench `save` statement rules.
- PWL syntax guardrails.
- Bridge wrapper behavior and dual-suite unit paths.
- Runner syntax.

## Track 2: Strict EVAS Gold Validation

Use this as the fast local gate for changed or new gold tasks.

```bash
python3 runners/run_gold_suite.py \
  --family end-to-end \
  --output-root results/<run-name>
```

For a broader family run:

```bash
python3 runners/run_gold_suite.py \
  --family end-to-end \
  --family spec-to-va \
  --family bugfix \
  --family tb-generation \
  --output-root results/<run-name>
```

For a targeted task:

```bash
python3 runners/run_gold_suite.py \
  --family end-to-end \
  --task <task_id> \
  --output-root results/<run-name>
```

Primary output:

- `results/<run-name>/summary.json`
- per-task EVAS result folders

Pass condition:

- `status == PASS` for promoted gold tasks.
- Axis rates should be interpreted as `dut_compile`, `tb_compile`, and
  `sim_correct`.

## Track 3: EVAS Plus Spectre Dual Validation

Use this for paper-facing gold promotion and broad parity gates.

Preflight:

```bash
./scripts/check_bridge_ready.sh --json
```

Recommended dual run:

```bash
./scripts/run_with_bridge.sh \
  python3 runners/run_gold_dual_suite.py \
  --family end-to-end \
  --output-root results/<run-name>
```

For all current families:

```bash
./scripts/run_with_bridge.sh \
  python3 runners/run_gold_dual_suite.py \
  --family end-to-end \
  --family spec-to-va \
  --family bugfix \
  --family tb-generation \
  --output-root results/<run-name>
```

Why the wrapper matters:

- `runners/run_gold_dual_suite.py` blocks direct invocation by default.
- The wrapper sets `VAEVAS_BRIDGE_WRAPPER=1`, runs bridge preflight, starts the
  temporary tunnel, and cleans it up.
- Set `VB_USE_SSH_CONFIG_JUMP=1` to let local `~/.ssh/config` provide
  `ProxyJump` when the bridge `.env` jump host is stale or unreachable.
- Direct runs need `--allow-direct-run` and should be reserved for controlled
  debugging.

Primary output:

- `results/<run-name>/summary.json`
- per-task EVAS result
- per-task Spectre result
- `tran_spectre.csv`
- bridge preflight diagnostics

Pass condition:

- Paper-facing gold tasks should pass both EVAS and Spectre.
- Broad parity gates must maintain zero EVAS PASS / Spectre FAIL binary
  mismatches on audited slices.
- Failure-label taxonomy is secondary to binary PASS/FAIL agreement.

## Track 4: Reporting And Compact Evidence

Generate durable summaries from local result payloads.

```bash
python3 runners/gen_manifest.py \
  --results-dir results/<run-name> \
  --output results/<run-name>/MANIFEST.md

python3 runners/gen_weekly_summary.py

python3 runners/gen_paper_stats.py

python3 runners/materialize_main120_inventory.py
```

Tracked conclusions should live in `tables/` or `docs/`. Raw `results/` and
`generated-*` directories are local artifacts unless promoted to named fixtures.

## Promotion Checklist

Before a benchmark task is promoted:

1. Static integrity tests pass.
2. Gold EVAS validation passes.
3. Gold Spectre validation passes for paper-facing tasks.
4. The result path is recorded in a compact table or doc.
5. Any EVAS/Spectre disagreement is either fixed or entered into the
   conformance backlog.

## Current Operational Gaps

| Gap | Effect | Next action |
| --- | --- | --- |
| Spectre depends on bridge, tunnel, and remote Cadence environment. | Full dual validation is not always locally runnable. | Keep wrapper path as the documented route and record preflight status. |
| main120 currently lives as result evidence, not a tracked task source split. | A 120/120 pass summary is not enough for benchmark release, review, or source-level regression. | Use `materialize_main120_inventory.py` to rebuild the provenance map before source materialization. |
| No standalone script named `strict_evas`. | Strictness is distributed across runner behavior, task metadata, and checker logic. | Treat `run_gold_suite.py` plus tests as the EVAS gate. |
| `run_examples_suite.py` is smoke-oriented. | It is useful for examples but not the main benchmark promotion gate. | Use `run_gold_suite.py` and `run_gold_dual_suite.py` for benchmark claims. |
| Some older docs reference missing helper scripts or stale task counts. | New agents may follow the wrong branch. | Prefer this file, `VAEVAS_MAINLINE_PLAN.md`, `VABENCH_TOPDOWN_FUNCTION_TAXONOMY.md`, and `VABENCH_MAIN120_MATERIALIZATION.*`. |

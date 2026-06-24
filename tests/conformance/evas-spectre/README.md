# EVAS/Spectre L0 Conformance Suite

This directory contains simulator conformance diagnostics, not scored vaBench
benchmark tasks. Each case isolates one EVAS/Spectre semantic boundary that is
too low-level to be a circuit-function task, but important enough to protect as
a regression.

## Boundary

- L0 conformance cases do not count toward model capability, benchmark
  coverage, bugfix claims, or broad parity denominators.
- L1/L2 vaBench tasks should test circuit behavior: transfer curves, sampled
  values, lock/recovery flows, control schedules, and measured metrics.
- When a benchmark row exposes EVAS/Spectre disagreement, Spectre remains the
  final judge for the benchmark row. The disagreement becomes EVAS core debt
  until a minimal L0 case is added and passes.

## Required Workflow For New Mismatches

1. Run dual evaluation and generate mismatch triage:

   ```bash
   PYTHONPATH=runners python3 runners/report_evas_spectre_mismatch_triage.py \
     --result-root results/<dual-run-root> \
     --tag <short-run-tag>
   ```

2. Inspect rows marked `evas_spectre_mismatch` or `parity`.
3. Reduce each unique simulator cause into a minimal case under this suite.
4. Add or update the EVAS regression that fixes the minimal case.
5. Rerun the affected benchmark rows and confirm:
   - `EVAS PASS / Spectre FAIL == 0`
   - `Spectre PASS / EVAS FAIL == 0`
   - no L0 case is counted in the scored benchmark denominator.

## Case Structure

Each case directory must include:

- `meta.json`: declares `asset_type=evas_spectre_conformance`, suite, axis,
  expected relation, and all denominator counts set to false.
- `gold/`: minimal Verilog-A and Spectre assets that reproduce the semantic.
- `checks.yaml`: machine-readable checker hook or manual validation note.
- `README.md`: explains the isolated semantic and why it is not a normal
  benchmark task.

## Current Axes

| Case | Axis | Why It Exists |
| --- | --- | --- |
| `cross_event_post_side_read` | event-sampling | Event-body reads at a `cross(...)` boundary must match Spectre post-side semantics. |
| `settling_done_boundary` | checker-boundary | Settling checks should avoid false pass/fail at the exact boundary sample. |
| `vco_timer0_startup` | timer-startup | Absolute/periodic timer startup behavior must match Spectre-facing clock generation. |
| `file_metric_writer_io_timing` | side-output-IO | File metrics written during simulation must be available to the checker at the same logical time. |

## Common Mismatch Families

| Family | Usual Fix |
| --- | --- |
| `evas_rejects_spectre_accepted_dut` | Add frontend/parser or runtime support, then lock the accepted Spectre construct as L0. |
| `spectre_rejects_evas_accepted_candidate` | Tighten EVAS parser/subset checks or wrapper rules; Spectre-compatible behavior wins. |
| `event_or_sampling_semantics` | Minimize the event timing, source sampling, `cross`, `timer`, or `transition` behavior. |
| `waveform_parity_gate` | First audit checker windows and row density; if semantics truly differ, create L0. |

The intent is to stop one-off patches: every new EVAS/Spectre disagreement
should become a named, minimal regression before the benchmark result is used
as evidence.

# B3 Conformance Plan

Date: 2026-05-15

## Purpose

D004-B3 covers historical fixed-only `*_bugfix` rows where the useful issue is
EVAS/Spectre semantics rather than a reviewed model-level repair pair. These
assets live outside `tasks/` and are excluded from normal vaBench denominators.

## Assets Added

| Asset | Source main120 row | Axis | Expected relation | Why B3 |
| --- | --- | --- | --- | --- |
| `conformance/evas-spectre/file_metric_writer_io_timing` | `vbm1_file_metric_writer_bugfix` | `checker-semantics` | `binary_outcome_equal` | Validates file metric side effects and artifact parsing, not a circuit repair. |
| `conformance/evas-spectre/settling_done_boundary` | `vbm1_settling_time_measurement_tb_bugfix` | `solver-time-sampling` | `binary_outcome_equal` | Validates a strict `$abstime > 120 ns` measurement boundary, not a DUT bugfix. |
| `conformance/evas-spectre/vco_timer0_startup` | `vbm1_vco_phase_integrator_bugfix` | `event-ordering` | `waveform_equivalent` | Validates `initial_step` plus coincident `timer(0,1n)` startup ordering. |

## Count Policy

Each asset uses:

```json
{
  "asset_type": "evas_spectre_conformance",
  "suite": "evas-spectre",
  "counts": {
    "model_capability": false,
    "benchmark_coverage": false,
    "bugfix_claim": false,
    "broad_parity_denominator": false
  }
}
```

This keeps the public benchmark story clean:

- no B3 conformance case is a normal `bugfix` row;
- no B3 conformance case contributes to model capability pass rates;
- no B3 conformance case contributes to broad vaBench coverage counts;
- broad EVAS/Spectre parity remains measured on `vaBench-main`, while these
  assets diagnose one simulator semantic at a time.

## Runner Integration Needed

The current source drop defines the conformance contracts and minimal gold
fixtures. The leader integration should add a separate conformance runner or
runner mode that:

1. discovers `conformance/evas-spectre/**/meta.json`;
2. validates each meta file against `schemas/conformance.schema.json`;
3. runs the listed gold testbench on EVAS and Spectre;
4. dispatches to the asset-specific structured checker from `checks.yaml`;
5. writes reports outside normal vaBench result directories, for example
   `reports/evas-spectre-conformance/<run-id>/`;
6. rejects any attempt to aggregate these assets into normal vaBench task
   statistics.

## Checker Hooks

| Asset | Checker hook |
| --- | --- |
| `file_metric_writer_io_timing` | Capture file artifacts from the simulator run directory; parse the first numeric token after `cross`; compare to `30.5 ns`; compare `done` waveform before and after the crossing. |
| `settling_done_boundary` | Sample `done` and `vout` at fixed safe times around the strict boundary; avoid final-row, row-count, and endpoint-only checks. |
| `vco_timer0_startup` | Compare the first saved `phase` sample to the analytic `0.039 V` timer update; require `clk` low at startup; report early waveform drift separately. |

## Promotion Guidance

The underlying functions may still become normal vaBench tasks through other
families:

- file metric writing can become a measurement or `tb-generation` task if the
  public prompt explicitly asks for file-output semantics;
- settling-time measurement can become a `tb-generation` or `end-to-end`
  measurement task with safe observables;
- VCO phase integration can become `spec-to-va` or `end-to-end` using
  post-startup phase-span and edge-count metrics.

They should not be called `bugfix` unless a separate bad source is reconstructed
and reviewed with buggy-fail/fixed-pass evidence on both EVAS and Spectre.

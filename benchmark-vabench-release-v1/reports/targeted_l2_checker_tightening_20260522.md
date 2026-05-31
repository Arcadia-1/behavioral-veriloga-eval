# Targeted L2 Checker Tightening Evidence

Date: 2026-05-22

Scope: targeted rerun for the two L2 e2e rows whose checker definitions were tightened.

Full dual refresh required: `false`

Reason: gold Verilog-A and Spectre testbenches were not changed; only two checker definitions and prompt contracts were tightened.

Evidence source: `/private/tmp/vaevas_l2_dual_audit_20260522/summary.json`

## Summary

| Metric | Value |
| --- | ---: |
| tasks total | 2 |
| pass count | 2 |
| fail count | 0 |
| EVAS PASS / Spectre FAIL | 0 |
| bridge profile | `ci` |

## Rerun Rows

| Release Entry | Source Task | Result | Evidence |
| --- | --- | --- | --- |
| `vbr1_l2_event_controller:e2e` | `simultaneous_event_order_smoke` | `PASS` | ref edges at the expected grid and plateau levels `[0.18, 0.36, 0.54, 0.72]` passed in EVAS and Spectre; waveform parity passed. |
| `vbr1_l2_measurement_flow:e2e` | `final_step_file_metric_smoke` | `PASS` | metric levels `[0.225, 0.45, 0.675, 0.9]` and `candidate.out` with `count=4 metric=1.000` passed in EVAS and Spectre; waveform parity passed. |

## Boundary

This report is targeted evidence for the two checker-tightened L2 e2e rows only. The historical full-release dual certification remains in `benchmark-vabench-release-v1/reports/dual_certification.json`; do not present this targeted report as a full release dual refresh.

# vaBench Release Dual Rerun Staging Manifest

Date: 2026-05-23

This manifest lists runnable staging bundles prepared from
`dual_rerun_queue.json`. It is an execution input, not simulator pass evidence.

## Summary

| Metric | Count |
| --- | ---: |
| queue rows | 6 |
| queue rows with ready primary bundle | 6 |
| staged bundles | 7 |
| ready bundles | 7 |
| blocked bundles | 0 |

## Variant Counts

| Variant | Count |
| --- | ---: |
| `buggy` | 1 |
| `fixed` | 1 |
| `gold` | 5 |

## Bundles

| Entry | Form | Variant | Status | Staged task |
| --- | --- | --- | --- | --- |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct03_20260523/vbr1_l1_sample_and_hold_with_droop_leakage/dut/gold` |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct03_20260523/vbr1_l1_sample_and_hold_with_droop_leakage/tb/gold` |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct03_20260523/vbr1_l1_sample_and_hold_with_droop_leakage/bugfix/fixed` |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `buggy` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct03_20260523/vbr1_l1_sample_and_hold_with_droop_leakage/bugfix/buggy` |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct03_20260523/vbr1_l1_sample_and_hold_with_droop_leakage/e2e/gold` |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct03_20260523/vbr1_l2_converter_front_end/tb/gold` |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct03_20260523/vbr1_l2_converter_front_end/e2e/gold` |

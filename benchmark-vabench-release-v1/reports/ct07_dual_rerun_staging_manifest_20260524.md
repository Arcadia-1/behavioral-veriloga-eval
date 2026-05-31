# vaBench Release Dual Rerun Staging Manifest

Date: 2026-05-24

This manifest lists runnable staging bundles prepared from
`dual_rerun_queue.json`. It is an execution input, not simulator pass evidence.

## Summary

| Metric | Count |
| --- | ---: |
| queue rows | 4 |
| queue rows with ready primary bundle | 4 |
| staged bundles | 5 |
| ready bundles | 5 |
| blocked bundles | 0 |

## Variant Counts

| Variant | Count |
| --- | ---: |
| `buggy` | 1 |
| `fixed` | 1 |
| `gold` | 3 |

## Bundles

| Entry | Form | Variant | Status | Staged task |
| --- | --- | --- | --- | --- |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct07_20260524/vbr1_l1_element_shuffler/dut/gold` |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct07_20260524/vbr1_l1_element_shuffler/tb/gold` |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct07_20260524/vbr1_l1_element_shuffler/bugfix/fixed` |
| `vbr1_l1_element_shuffler` | `bugfix` | `buggy` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct07_20260524/vbr1_l1_element_shuffler/bugfix/buggy` |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ready` | `benchmark-vabench-release-v1/rerun_staging_ct07_20260524/vbr1_l1_element_shuffler/e2e/gold` |

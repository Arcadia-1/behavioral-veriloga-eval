# vaBench Release EVAS-Only Staging Audit

Status: `complete`
Manifest: `benchmark-vabench-release-v1/reports/full_evas_only_audit_staging_manifest_20260527.json`
Output root: `results/vabench-release-v1-full-evas-only-audit-20260527-fixcheck`

## Summary

| Metric | Count |
| --- | ---: |
| selected bundles | 12 |
| completed bundles | 12 |
| PASS | 6 |
| non-PASS | 6 |
| expected met | 7 |
| expected miss | 5 |

## Raw Status Counts

| Status | Count |
| --- | ---: |
| `FAIL_INFRA` | 5 |
| `FAIL_SIM_CORRECTNESS` | 1 |
| `PASS` | 6 |

## Expected Miss Rows

| Entry | Form | Variant | Expected | Actual | Notes |
| --- | --- | --- | --- | --- | --- |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `buggy` | `fail` | `FAIL_INFRA` | evas_only_exception=TimeoutExpired: Command '['/Users/bucketsran/bin/evas', 'simulate', 'tb_pfd_reset_race_ref.scs', '-o', '/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-release-v1-full-evas-only-a |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `pass` | `FAIL_INFRA` | evas_only_exception=TimeoutExpired: Command '['/Users/bucketsran/bin/evas', 'simulate', 'tb_pfd_reset_race_ref.scs', '-o', '/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-release-v1-full-evas-only-a |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `pass` | `FAIL_INFRA` | evas_only_exception=TimeoutExpired: Command '['/Users/bucketsran/bin/evas', 'simulate', 'tb_pfd_reset_race_ref.scs', '-o', '/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-release-v1-full-evas-only-a |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `pass` | `FAIL_INFRA` | evas_only_exception=TimeoutExpired: Command '['/Users/bucketsran/bin/evas', 'simulate', 'tb_pfd_reset_race_ref.scs', '-o', '/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-release-v1-full-evas-only-a |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `pass` | `FAIL_INFRA` | evas_only_exception=TimeoutExpired: Command '['/Users/bucketsran/bin/evas', 'simulate', 'tb_pfd_reset_race_ref.scs', '-o', '/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-release-v1-full-evas-only-a |

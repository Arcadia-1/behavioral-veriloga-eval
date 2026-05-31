# vaBench Release EVAS-Only Staging Audit

Status: `complete`
Manifest: `benchmark-vabench-release-v1/reports/full_evas_only_audit_staging_manifest_20260527.json`
Output root: `results/vabench-release-v1-full-evas-only-audit-20260527-r1`

## Summary

| Metric | Count |
| --- | ---: |
| selected bundles | 325 |
| completed bundles | 325 |
| PASS | 261 |
| non-PASS | 64 |
| expected met | 314 |
| expected miss | 11 |

## Raw Status Counts

| Status | Count |
| --- | ---: |
| `FAIL_INFRA` | 5 |
| `FAIL_SIM_CORRECTNESS` | 59 |
| `PASS` | 261 |

## Expected Miss Rows

| Entry | Form | Variant | Expected | Actual | Notes |
| --- | --- | --- | --- | --- | --- |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `buggy` | `fail` | `FAIL_INFRA` | evas_only_exception=TimeoutExpired: Command '['/Users/bucketsran/bin/evas', 'simulate', 'tb_pfd_reset_race_ref.scs', '-o', '/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-release-v1-full-evas-only-a |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `pass` | `FAIL_INFRA` | evas_only_exception=TimeoutExpired: Command '['/Users/bucketsran/bin/evas', 'simulate', 'tb_pfd_reset_race_ref.scs', '-o', '/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-release-v1-full-evas-only-a |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `pass` | `FAIL_INFRA` | evas_only_exception=TimeoutExpired: Command '['/Users/bucketsran/bin/evas', 'simulate', 'tb_pfd_reset_race_ref.scs', '-o', '/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-release-v1-full-evas-only-a |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `pass` | `FAIL_INFRA` | evas_only_exception=TimeoutExpired: Command '['/Users/bucketsran/bin/evas', 'simulate', 'tb_pfd_reset_race_ref.scs', '-o', '/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-release-v1-full-evas-only-a |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `pass` | `FAIL_INFRA` | evas_only_exception=TimeoutExpired: Command '['/Users/bucketsran/bin/evas', 'simulate', 'tb_pfd_reset_race_ref.scs', '-o', '/Users/bucketsran/Documents/TsingProject/vaEvas/behavioral-veriloga-eval/results/vabench-release-v1-full-evas-only-a |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `pass` | `FAIL_SIM_CORRECTNESS` | returncode=0; soft_limiter_high_compression=0.468 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `pass` | `FAIL_SIM_CORRECTNESS` | returncode=0; soft_limiter_high_compression=0.468 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `pass` | `FAIL_SIM_CORRECTNESS` | returncode=0; soft_limiter_high_compression=0.468 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `pass` | `FAIL_SIM_CORRECTNESS` | returncode=0; soft_limiter_high_compression=0.468 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `pass` | `FAIL_SIM_CORRECTNESS` | returncode=0; amp_filter_metric_not_preamp_target early=0.788 late=0.801 low=0.105 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `pass` | `FAIL_SIM_CORRECTNESS` | returncode=0; amp_filter_metric_not_preamp_target early=0.788 late=0.801 low=0.105 |

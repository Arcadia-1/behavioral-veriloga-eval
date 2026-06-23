# vaBench 300 v1.1 Fresh Spectre Rerun

- date: `2026-06-23`
- status: `pass`
- source summary sha256: `88677ee4c97063da7db1df486b8c1530edc6ac67c3d36c58de9de67145236d3e`
- rows: 29
- PASS: 29
- non-PASS: 0
- parity passed: 29
- EVAS PASS / Spectre FAIL: 0
- total wall time: 168.01728478999996 s

This report imports compact evidence from the fresh v1.1 EVAS/Spectre rerun.
Raw simulator directories remain outside the repository; this file is the versioned certification summary.
Score-denominator admission is tracked separately in `benchmark-vabench-release-v1/reports/vabench_300_v11_score_admission.json`.

## Rows

| Task | Raw | EVAS | Spectre | Parity | max RMSE V | max abs V | Evidence timing |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `bootstrapped_sample_switch:bugfix` | `PASS` | `PASS` | `PASS` | `passed` | 0.00017312438786749485 | 0.0005914202747334674 | 6.900458625 |
| `bootstrapped_sample_switch:dut` | `PASS` | `PASS` | `PASS` | `passed` | 0.00017312438786749485 | 0.0005914202747334674 | 6.950340874 |
| `bootstrapped_sample_switch:e2e` | `PASS` | `PASS` | `PASS` | `passed` | 0.00017312438786749485 | 0.0005914202747334674 | 5.387952958000001 |
| `bootstrapped_sample_switch:tb` | `PASS` | `PASS` | `PASS` | `passed` | 0.00017312438786749485 | 0.0005914202747334674 | 5.863433958 |
| `sigma_delta_modulator_loop:bugfix` | `PASS` | `PASS` | `PASS` | `passed` | 0.00021235652004672275 | 0.0007684988154467165 | 4.9059923749999985 |
| `sigma_delta_modulator_loop:dut` | `PASS` | `PASS` | `PASS` | `passed` | 0.00021235652004672275 | 0.0007684988154467165 | 5.610083417000002 |
| `sigma_delta_modulator_loop:e2e` | `PASS` | `PASS` | `PASS` | `passed` | 0.00021235652004672275 | 0.0007684988154467165 | 5.637841333000001 |
| `sigma_delta_modulator_loop:tb` | `PASS` | `PASS` | `PASS` | `passed` | 0.00021235652004672275 | 0.0007684988154467165 | 5.520269292000002 |
| `bandgap_startup_trim:bugfix` | `PASS` | `PASS` | `PASS` | `passed` | 1.3684221474657381e-05 | 5.310010620002137e-05 | 6.082206875000001 |
| `bandgap_startup_trim:dut` | `PASS` | `PASS` | `PASS` | `passed` | 1.3684221474657381e-05 | 5.310010620002137e-05 | 6.2578889179999955 |
| `bandgap_startup_trim:e2e` | `PASS` | `PASS` | `PASS` | `passed` | 1.3684221474657381e-05 | 5.310010620002137e-05 | 4.443072165999997 |
| `bandgap_startup_trim:tb` | `PASS` | `PASS` | `PASS` | `passed` | 1.3684221474657381e-05 | 5.310010620002137e-05 | 4.6378271669999975 |
| `fractional_n_pll_divider:bugfix` | `PASS` | `PASS` | `PASS` | `passed` | 6.254037520877988e-05 | 0.00024606882984268275 | 6.018033375000002 |
| `fractional_n_pll_divider:dut` | `PASS` | `PASS` | `PASS` | `passed` | 6.254037520877988e-05 | 0.00024606882984268275 | 4.899619541 |
| `fractional_n_pll_divider:e2e` | `PASS` | `PASS` | `PASS` | `passed` | 6.254037520877988e-05 | 0.00024606882984268275 | 4.533563417000003 |
| `fractional_n_pll_divider:tb` | `PASS` | `PASS` | `PASS` | `passed` | 6.254037520877988e-05 | 0.00024606882984268275 | 4.611735959000001 |
| `metastability_window_comparator:bugfix` | `PASS` | `PASS` | `PASS` | `passed` | 6.996106081281078e-05 | 0.00023075193105326353 | 5.992629790999999 |
| `metastability_window_comparator:dut` | `PASS` | `PASS` | `PASS` | `passed` | 6.996106081281078e-05 | 0.00023075193105326353 | 6.001361541000001 |
| `metastability_window_comparator:e2e` | `PASS` | `PASS` | `PASS` | `passed` | 6.996106081281078e-05 | 0.00023075193105326353 | 4.693563875000002 |
| `metastability_window_comparator:tb` | `PASS` | `PASS` | `PASS` | `passed` | 6.996106081281078e-05 | 0.00023075193105326353 | 4.992050624000001 |
| `quadrature_iq_imbalance_corrector:bugfix` | `PASS` | `PASS` | `PASS` | `passed` | 0.00028277231891682696 | 0.000985167651710972 | 7.443841875000004 |
| `quadrature_iq_imbalance_corrector:dut` | `PASS` | `PASS` | `PASS` | `passed` | 0.00028277231891682696 | 0.000985167651710972 | 6.632960625999992 |
| `quadrature_iq_imbalance_corrector:e2e` | `PASS` | `PASS` | `PASS` | `passed` | 0.00028277231891682696 | 0.000985167651710972 | 5.912662499999996 |
| `quadrature_iq_imbalance_corrector:tb` | `PASS` | `PASS` | `PASS` | `passed` | 0.00028277231891682696 | 0.000985167651710972 | 5.346183124999996 |
| `time_interleaved_adc_mismatch:bugfix` | `PASS` | `PASS` | `PASS` | `passed` | 0.00042846142389080894 | 0.0017602753706568164 | 6.272437542000006 |
| `time_interleaved_adc_mismatch:dut` | `PASS` | `PASS` | `PASS` | `passed` | 0.00042846142389080894 | 0.0017602753706568164 | 6.140744208000015 |
| `time_interleaved_adc_mismatch:e2e` | `PASS` | `PASS` | `PASS` | `passed` | 0.00042846142389080894 | 0.0017602753706568164 | 4.649721874999997 |
| `time_interleaved_adc_mismatch:tb` | `PASS` | `PASS` | `PASS` | `passed` | 0.00042846142389080894 | 0.0017602753706568164 | 5.728594873999995 |
| `cppll_tracking_frequency_step_reacquire:bugfix` | `PASS` | `PASS` | `PASS` | `passed` | 3.15112716196203e-05 | 0.0001675003350048998 | 7.363045249999999 |

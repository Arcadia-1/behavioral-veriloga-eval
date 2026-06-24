# vaBench v2 Gold Spectre Mini-Cert (2026-06-24)

- Status: `PASS`
- Rows: `5/5` PASS
- Spectre backend: `bridge`
- Spectre mode: `ax`
- Raw output root: `/private/tmp/vabench_v2_gold_spectre_mini_cert_20260624_r3`

| task | status | EVAS | Spectre | Spectre behavior | parity | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `PASS` | `PASS` | `PASS` | `1.0` | `passed` | spectre_rows=16591 |
| `vbr1_l1_window_comparator_detector:tb` | `PASS` | `PASS` | `PASS` | `1.0` | `passed` | spectre_rows=72 |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | `PASS` | `PASS` | `PASS` | `1.0` | `passed` | spectre_rows=223 |
| `vbr1_l1_first_order_lowpass:bugfix` | `PASS` | `PASS` | `PASS` | `1.0` | `passed` | spectre_rows=612 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow:e2e` | `PASS` | `PASS` | `PASS` | `1.0` | `passed` | runner_diagnostic_errors=convergence failure; spectre.out:0_errors; spectre_rows=15067 |

Admission rule: this mini-cert is a gold-task smoke certificate for the five v2 representative forms. Spectre remains the final judge; raw simulator outputs stay under `/private/tmp` and are not committed.

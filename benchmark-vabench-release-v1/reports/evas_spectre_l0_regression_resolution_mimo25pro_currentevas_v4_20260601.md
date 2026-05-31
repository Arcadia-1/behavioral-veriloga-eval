# EVAS/Spectre L0 Regression Resolution

Generated: 2026-06-01

Scope: MiMo 2.5-pro highout32k full236 refresh with current EVAS.

## Current Result

| Metric | Value |
| --- | ---: |
| scored forms | 236 |
| completed dual rows | 228 |
| skipped generation rows | 8 |
| Spectre checker pass rows | 113 |
| strict dual pass rows | 113 |
| EVAS PASS / Spectre FAIL rows | 0 |
| Spectre PASS / EVAS FAIL rows | 0 |
| waveform parity gate rows | 0 |

Evidence:

- Candidate run: `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260601-full236-highout32k-currentevas-v4-dual`
- Triage report: `benchmark-vabench-release-v1/reports/evas_spectre_mismatch_triage_mimo25pro_full236_highout32k_currentevas_v4_20260601.json`

## Resolved Findings

| Finding | Classification | Root cause | Current status |
| --- | --- | --- | --- |
| `vbm1_resettable_counter_divider_tb` waveform parity gate | EVAS source scheduling semantics | EVAS treated no-period Spectre pulse as DC high; Spectre treats it as a nonperiodic one-shot pulse. | Resolved by EVAS pulse one-shot semantics; full236 v4 has zero parity gate rows. |
| calibration deadband boundary false negative | checker window calibration | Both simulators followed the same trim sequence, but exact 0.120 V span threshold was too brittle for transition sampling. | Resolved by 1e-6 V boundary tolerance in release checker. |
| `vbr1_l1_pipeline_adc_stage:bugfix` Spectre PASS / EVAS FAIL | EVAS Verilog-A identifier compatibility | EVAS used case-insensitive parameter/port collision detection; Verilog-A identifiers are case-sensitive, so `VDD` and `vdd` are distinct. | Resolved by case-sensitive preflight; full236 v4 has zero Spectre PASS / EVAS FAIL rows. |
| PWL inline arithmetic and too-few instance terminals | EVAS front-end compatibility | EVAS accepted Spectre-rejected `wave=[...]` arithmetic and under-arity positional instances. | Resolved by parser and instance-arity preflight; full236 v4 has zero EVAS PASS / Spectre FAIL rows. |

## L0 Regression Coverage

- `tests/test_netlist.py::TestAddSpectreSourceDegenerateCases::test_pulse_missing_period_but_different_vals_warns`
- `tests/test_netlist.py::TestAddSpectreSourceDegenerateCases::test_nonperiodic_pulse_width_falls_once`
- `tests/test_netlist.py::TestSaveAndPwlRegressions::test_pwl_inline_arithmetic_rejected`
- `tests/test_netlist.py::TestRunnerSpectreCompatibility::test_instance_terminal_count_mismatch_fails`
- `tests/test_netlist.py::TestRunnerSpectreCompatibility::test_case_distinct_parameter_and_port_names_are_allowed`

Conclusion: the remaining waveform parity investigation was an EVAS source-semantics issue, not a benchmark task failure. The exact-threshold calibration case was checker-window calibration. The current full236 refresh has no EVAS/Spectre binary mismatch and no waveform parity gate rows.

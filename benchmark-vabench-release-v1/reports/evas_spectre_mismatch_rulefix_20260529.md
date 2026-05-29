# EVAS/Spectre Mismatch Rulefix Rerun - 2026-05-29

Scope: targeted rerun of the five previously exposed Spectre PASS / EVAS FAIL rows from the current DeepSeek and MiMo baselines.

Repair rule applied:

- Fix a general parser/source/elaboration/event/checker semantic class.
- Add or run an atomic regression for the semantic class.
- Do not add EVAS-core branches keyed by task id, model id, module name, or checker note.
- Calibrate checker windows only after EVAS and Spectre are semantically aligned.

Implemented semantic fixes:

| Class | Fix | Regression evidence |
|---|---|---|
| Spectre source semantics | `100M` now parses as 100 MHz while `900m` remains 0.9; transient sine uses canonical `sinedc`/`ampl` and does not treat `vo`/`va`/`offset`/`amplitude` as waveform aliases. | `EVAS/tests/test_netlist.py` |
| Verilog-A elaboration | Module-scope real initializers can reference earlier parameters and variables. | `EVAS/tests/test_engine.py` |
| `cross()` scheduling | Same-step cross event bodies are protected from retrograde source-order overwrites; later crossing effects cannot be overwritten by an earlier crossing discovered later in source order. | `EVAS/tests/test_engine.py` |
| Checker windowing | RSSI checker uses time-weighted window means instead of point-count means so Spectre/EVAS adaptive sample density does not decide correctness. | `tests/test_vabench_function_checker_regressions.py` |

Targeted rerun results:

| Baseline | Row | Result after fix | Interpretation |
|---|---|---|---|
| DeepSeek v4-pro | `vbr1_l1_bias_voltage_generator_with_enable_trim:dut` | strict dual PASS | EVAS false negative fixed by elaboration support. |
| DeepSeek v4-pro | `vbr1_l1_rf_mixer_downconverter_macro:tb` | strict dual PASS | EVAS false negative fixed by Spectre sine/source semantics. |
| MiMo v2.5-pro | `vbr1_l1_bandgap_reference_macro_model:dut` | strict dual PASS | EVAS false negative fixed by chronological cross-event behavior. |
| MiMo v2.5-pro | `vbr1_l1_rf_mixer_downconverter_macro:tb` | strict dual PASS | EVAS false negative fixed by Spectre sine/source semantics. |
| MiMo v2.5-pro | `vbr1_l1_log_rssi_power_detector:tb` | EVAS FAIL / Spectre FAIL | Old Spectre pass was a checker sampling-density artifact; time-weighted checker now consistently rejects the non-loglike waveform (`small/mid/high=0.120/0.714/0.720`). |

Summary:

| Target slice | Rows | Strict dual pass | EVAS PASS / Spectre FAIL | Spectre PASS / EVAS FAIL |
|---|---:|---:|---:|---:|
| DeepSeek mismatch rerun | 2 | 2 | 0 | 0 |
| MiMo mismatch rerun | 3 | 2 | 0 | 0 |

Result roots:

- `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260529-evasrulefix-mismatch2-dual/summary.json`
- `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260529-evasrulefix-mismatch3-dual/summary.json`

Validation:

- `PYTHONPATH=. python3 -m pytest tests/test_netlist.py tests/test_compiler.py tests/test_engine.py -q` in `EVAS`: 360 passed.
- `PYTHONPATH=runners python3 -m pytest tests/test_vabench_function_checker_regressions.py -q` in `behavioral-veriloga-eval`: 50 passed.

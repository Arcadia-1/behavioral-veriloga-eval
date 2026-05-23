# vaBench Release Tasks By Circuit Type

This directory groups release benchmark entries by the circuit-type IDs used for
manual prompt and checker audit. Each `vbr1_*` entry remains a self-contained
release benchmark with `release_entry.json` and per-form `forms/*` assets.

| ID | Directory | Circuit type | Entries |
| --- | --- | --- | ---: |
| CT01 | `CT01_data_converters` | Data Converters | 18 |
| CT02 | `CT02_comparators_and_decision_circuits` | Comparators and Decision Circuits | 8 |
| CT03 | `CT03_sample_hold_and_analog_memory` | Sample, Hold, and Analog Memory | 4 |
| CT04 | `CT04_analog_behavioral_signal_conditioning` | Analog Behavioral Signal Conditioning | 7 |
| CT05 | `CT05_pll_clock_event_timing` | PLL / Clock / Event Timing | 13 |
| CT07 | `CT07_calibration_dem_and_control` | Calibration, DEM, and Control | 9 |
| CT08 | `CT08_measurement_and_testbench_instrumentation` | Measurement and Testbench Instrumentation | 7 |
| CT09 | `CT09_stimulus_and_sources` | Stimulus and Sources | 6 |

Use the category folders for human review. Machine-readable manifests and
report paths use the same canonical category layout.

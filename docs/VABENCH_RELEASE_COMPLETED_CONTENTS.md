# vaBench Release Completed Benchmark Contents

Date: 2026-05-24

This note records the benchmark contents currently materialized in the clean
`vabench-release-v1` package after the 79-entry expansion. The package manifest
and release reports remain the source of truth for certification and scoring.

## Evidence Sources

- `benchmark-vabench-release-v1/MANIFEST.json`
- `benchmark-vabench-release-v1/reports/release_status.json`
- `benchmark-vabench-release-v1/reports/score_denominator_manifest.json`
- `benchmark-vabench-release-v1/reports/schema_validation.json`

## Completion Snapshot

| Item | Count | Meaning |
| --- | ---: | --- |
| Release entries | 79 | Top-level L1/L2 benchmark entries: core circuit functions plus auxiliary measurement/stimulus support entries. |
| L1 entries | 62 | Single-function model-capability tasks. |
| L2 entries | 17 | Complete-circuit or chain-level flows. |
| Release task forms | 271 | Materialized `dut`, `tb`, `bugfix`, and/or `e2e` forms. |
| Core content-denominator entries | 66 | Certified core entries allowed to enter the main benchmark score. |
| Core content-denominator forms | 236 | Materialized forms attached to scored core entries. |
| Support suite entries/forms | 13 / 35 | Certified support rows reported separately from the core score. |
| Static-certified entries/forms | 79 / 271 | Prompt/meta/checks/gold/static integrity currently pass. |
| EVAS/Spectre-certified entries/forms | 79 / 271 | Full release dual validation passes. |
| Pending dual entries/forms | 0 / 0 | No current release forms await EVAS/Spectre certification. |
| EVAS PASS / Spectre FAIL | 0 | Hard parity mismatch count in current audited release reports. |
| Scored entries/forms | 66 / 236 | Enabled for certified `track=core`; support remains excluded. |

## Form Counts

| Form | Count | Scope |
| --- | ---: | --- |
| `dut` | 59 | Materialized release form. |
| `tb` | 79 | Materialized release form. |
| `bugfix` | 54 | Materialized release form. |
| `e2e` | 79 | Materialized release form. |

## Category Summary

| Category | Entries | L1 | L2 | Forms |
| --- | ---: | ---: | ---: | ---: |
| Data Converter Models | 13 | 9 | 4 | 44 |
| Comparator and Decision Circuits | 8 | 7 | 1 | 30 |
| PLL Clock and Timing Systems | 10 | 8 | 2 | 36 |
| Calibration, DEM, and Control | 7 | 6 | 1 | 26 |
| Baseband Signal Conditioning | 8 | 7 | 1 | 30 |
| Sampling and Analog Memory | 5 | 4 | 1 | 18 |
| Bias Reference and Power Management | 8 | 6 | 2 | 28 |
| RF and AFE Behavioral Macromodels | 7 | 5 | 2 | 24 |
| Measurement Instrumentation Flows | 7 | 5 | 2 | 17 |
| Stimulus and Source Generators | 6 | 5 | 1 | 18 |

## Core/Support Split

| Role | Categories | Entries | Paper wording |
| --- | --- | ---: | --- |
| Core circuit coverage | Data Converter Models; Comparator and Decision Circuits; PLL Clock and Timing Systems; Calibration, DEM, and Control; Baseband Signal Conditioning; Sampling and Analog Memory; Bias Reference and Power Management; RF and AFE Behavioral Macromodels | 66 | Use for claims about analog/mixed-signal circuit-function coverage. |
| Support coverage | Measurement Instrumentation Flows; Stimulus and Source Generators | 13 | Report as reusable measurement, instrumentation, and stimulus/source modeling coverage. Do not use to inflate the core circuit count. |

## Functions By Category

All entries below are materialized and static-certified. Measurement and
stimulus/source rows are benchmark support entries, not core analog signal-path
or decision-circuit rows. All 271 forms are currently static-certified and
EVAS/Spectre-certified.

| Category | Level | Function | Forms |
| --- | --- | --- | --- |
| Data Converter Models | L1 | Simple 4-bit binary-coded DAC | `dut`, `tb`, `bugfix`, `e2e` |
| Data Converter Models | L1 | Unit-element thermometer DAC | `dut`, `tb`, `bugfix`, `e2e` |
| Data Converter Models | L1 | Segmented DAC | `dut`, `tb`, `bugfix`, `e2e` |
| Data Converter Models | L1 | Thermometer-code decoder | `dut`, `tb`, `bugfix`, `e2e` |
| Data Converter Models | L1 | Clocked ADC quantizer | `dut`, `tb`, `bugfix`, `e2e` |
| Data Converter Models | L1 | Capacitive/weighted SAR feedback DAC | `dut`, `tb`, `bugfix`, `e2e` |
| Data Converter Models | L1 | DAC mismatch/unit-weighting model | `dut`, `tb`, `bugfix`, `e2e` |
| Data Converter Models | L1 | SAR logic | `dut`, `tb`, `bugfix`, `e2e` |
| Data Converter Models | L1 | Pipeline ADC MDAC stage | `dut`, `tb`, `bugfix`, `e2e` |
| Data Converter Models | L2 | Converter static linearity measurement flow | `tb`, `e2e` |
| Data Converter Models | L2 | Weighted SAR ADC/DAC loop | `tb`, `e2e` |
| Data Converter Models | L2 | Flash ADC mini-array | `tb`, `e2e` |
| Data Converter Models | L2 | Pipeline ADC residue chain | `tb`, `e2e` |
| Comparator and Decision Circuits | L1 | Threshold comparator | `dut`, `tb`, `bugfix`, `e2e` |
| Comparator and Decision Circuits | L1 | Propagation-delay comparator | `dut`, `tb`, `bugfix`, `e2e` |
| Comparator and Decision Circuits | L1 | Hysteresis comparator | `dut`, `tb`, `bugfix`, `e2e` |
| Comparator and Decision Circuits | L1 | Window comparator/detector | `dut`, `tb`, `bugfix`, `e2e` |
| Comparator and Decision Circuits | L1 | Offset comparator | `dut`, `tb`, `bugfix`, `e2e` |
| Comparator and Decision Circuits | L1 | StrongARM-style latch comparator | `dut`, `tb`, `bugfix`, `e2e` |
| Comparator and Decision Circuits | L1 | Comparator debounce latch | `dut`, `tb`, `bugfix`, `e2e` |
| Comparator and Decision Circuits | L2 | Single-ramp comparator offset measurement flow | `tb`, `e2e` |
| PLL Clock and Timing Systems | L1 | VCO phase integrator | `dut`, `tb`, `bugfix`, `e2e` |
| PLL Clock and Timing Systems | L1 | PFD UP/DN logic | `dut`, `tb`, `bugfix`, `e2e` |
| PLL Clock and Timing Systems | L1 | Bang-bang phase detector | `dut`, `tb`, `bugfix`, `e2e` |
| PLL Clock and Timing Systems | L1 | Digital phase accumulator with modulo wrap | `dut`, `tb`, `bugfix`, `e2e` |
| PLL Clock and Timing Systems | L1 | Clock divider | `dut`, `tb`, `bugfix`, `e2e` |
| PLL Clock and Timing Systems | L1 | Lock detector | `dut`, `tb`, `bugfix`, `e2e` |
| PLL Clock and Timing Systems | L1 | Voltage-domain charge-pump control abstraction | `dut`, `tb`, `bugfix`, `e2e` |
| PLL Clock and Timing Systems | L1 | Sampled loop-filter abstraction | `dut`, `tb`, `bugfix`, `e2e` |
| PLL Clock and Timing Systems | L2 | ADPLL lock/ratio-hop/timer flow | `tb`, `e2e` |
| PLL Clock and Timing Systems | L2 | CPPLL tracking and frequency-step reacquire flow | `tb`, `e2e` |
| Calibration, DEM, and Control | L1 | Trim-voltage generator | `dut`, `tb`, `bugfix`, `e2e` |
| Calibration, DEM, and Control | L1 | Gain trim controller | `dut`, `tb`, `bugfix`, `e2e` |
| Calibration, DEM, and Control | L1 | DWA/DEM encoder | `dut`, `tb`, `bugfix`, `e2e` |
| Calibration, DEM, and Control | L1 | Calibration deadband controller | `dut`, `tb`, `bugfix`, `e2e` |
| Calibration, DEM, and Control | L1 | Successive-approximation calibration/search FSM | `dut`, `tb`, `bugfix`, `e2e` |
| Calibration, DEM, and Control | L1 | Element shuffler | `dut`, `tb`, `bugfix`, `e2e` |
| Calibration, DEM, and Control | L2 | Complete calibration loop | `tb`, `e2e` |
| Baseband Signal Conditioning | L1 | First-order lowpass | `dut`, `tb`, `bugfix`, `e2e` |
| Baseband Signal Conditioning | L1 | Resettable integrator | `dut`, `tb`, `bugfix`, `e2e` |
| Baseband Signal Conditioning | L1 | Soft/hysteretic limiter | `dut`, `tb`, `bugfix`, `e2e` |
| Baseband Signal Conditioning | L1 | Precision rectifier/envelope detector | `dut`, `tb`, `bugfix`, `e2e` |
| Baseband Signal Conditioning | L1 | Higher-order filter | `dut`, `tb`, `bugfix`, `e2e` |
| Baseband Signal Conditioning | L1 | Slew-rate limiter | `dut`, `tb`, `bugfix`, `e2e` |
| Baseband Signal Conditioning | L1 | Programmable gain amplifier | `dut`, `tb`, `bugfix`, `e2e` |
| Baseband Signal Conditioning | L2 | Amplifier/filter chain | `tb`, `e2e` |
| Sampling and Analog Memory | L1 | Aperture-delay track-and-hold | `dut`, `tb`, `bugfix`, `e2e` |
| Sampling and Analog Memory | L1 | Sample-and-hold with droop/leakage | `dut`, `tb`, `bugfix`, `e2e` |
| Sampling and Analog Memory | L1 | Clocked sample-and-hold | `dut`, `tb`, `bugfix`, `e2e` |
| Sampling and Analog Memory | L1 | Acquisition-limited sample-and-hold | `dut`, `tb`, `bugfix`, `e2e` |
| Sampling and Analog Memory | L2 | Converter front-end | `tb`, `e2e` |
| Bias Reference and Power Management | L1 | Bandgap reference macromodel | `dut`, `tb`, `bugfix`, `e2e` |
| Bias Reference and Power Management | L1 | PTAT/CTAT reference generator | `dut`, `tb`, `bugfix`, `e2e` |
| Bias Reference and Power Management | L1 | Bias voltage generator with enable and trim | `dut`, `tb`, `bugfix`, `e2e` |
| Bias Reference and Power Management | L1 | LDO regulator macromodel | `dut`, `tb`, `bugfix`, `e2e` |
| Bias Reference and Power Management | L1 | UVLO/brownout detector | `dut`, `tb`, `bugfix`, `e2e` |
| Bias Reference and Power Management | L1 | Power-on reset detector | `dut`, `tb`, `bugfix`, `e2e` |
| Bias Reference and Power Management | L2 | Reference startup/enable flow | `tb`, `e2e` |
| Bias Reference and Power Management | L2 | LDO load-step recovery flow | `tb`, `e2e` |
| RF and AFE Behavioral Macromodels | L1 | LNA gain-compression macromodel | `dut`, `tb`, `bugfix`, `e2e` |
| RF and AFE Behavioral Macromodels | L1 | RF mixer/downconverter macromodel | `dut`, `tb`, `bugfix`, `e2e` |
| RF and AFE Behavioral Macromodels | L1 | Limiting amplifier front-end | `dut`, `tb`, `bugfix`, `e2e` |
| RF and AFE Behavioral Macromodels | L1 | Log/RSSI power detector | `dut`, `tb`, `bugfix`, `e2e` |
| RF and AFE Behavioral Macromodels | L1 | PA compression macromodel | `dut`, `tb`, `bugfix`, `e2e` |
| RF and AFE Behavioral Macromodels | L2 | I/Q downconversion chain | `tb`, `e2e` |
| RF and AFE Behavioral Macromodels | L2 | AGC receiver leveling loop | `tb`, `e2e` |
| Measurement Instrumentation Flows | L1 | Crossing metric writer (support/measurement) | `dut`, `tb`, `e2e` |
| Measurement Instrumentation Flows | L1 | Settling response measurement helper (support/measurement) | `tb`, `e2e` |
| Measurement Instrumentation Flows | L1 | Peak detector (support/measurement) | `dut`, `tb`, `bugfix`, `e2e` |
| Measurement Instrumentation Flows | L1 | Gain estimator (support/measurement) | `tb`, `e2e` |
| Measurement Instrumentation Flows | L1 | Edge interval timer (support/measurement) | `tb`, `e2e` |
| Measurement Instrumentation Flows | L2 | Measurement flow (support/measurement) | `tb`, `e2e` |
| Measurement Instrumentation Flows | L2 | Gain extraction/convergence measurement flow (support/measurement) | `tb`, `e2e` |
| Stimulus and Source Generators | L1 | PRBS stimulus/dither generator (support/stimulus) | `dut`, `tb`, `bugfix`, `e2e` |
| Stimulus and Source Generators | L1 | Periodic phase-ramp guard source (support/stimulus) | `dut`, `tb`, `e2e` |
| Stimulus and Source Generators | L1 | Burst clock source (support/stimulus) | `dut`, `tb`, `e2e` |
| Stimulus and Source Generators | L1 | Dither or noise-like deterministic source (support/stimulus) | `dut`, `tb`, `e2e` |
| Stimulus and Source Generators | L1 | Sine/periodic voltage source (support/stimulus) | `dut`, `tb`, `e2e` |
| Stimulus and Source Generators | L2 | Programmable stimulus sequencer (support/stimulus) | `tb`, `e2e` |

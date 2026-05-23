# vaBench Release Completed Benchmark Contents

Date: 2026-05-16

This note records the benchmark contents that are currently materialized in the
clean `vabench-release-v1` package. It answers a narrower question than the
score or paper-claim reports:

> Which top-level circuit functions already exist as benchmark tasks?

Content-audit note: the package still contains 80 materialized entries as
auditable assets, but five L2 entries are exact or semantic duplicate kernels
and are logically excluded from the strong benchmark content denominator until
they are rewritten.

## Evidence Sources

The authoritative package and certification evidence are:

- `benchmark-vabench-release-v1/MANIFEST.json`
- `benchmark-vabench-release-v1/reports/release_status.json`
- `benchmark-vabench-release-v1/reports/dual_certification.json`
- `benchmark-vabench-release-v1/reports/certification_matrix.json`
- `results/vabench-release-v1-dual-rerun-20260516-full-after-fixes/summary.json`

## Completion Snapshot

| Item | Count | Meaning |
| --- | ---: | --- |
| Release entries | 80 | Top-level L1/L2 circuit functions in the release package. |
| L1 entries | 60 | Single-function or single-block model-capability tasks. |
| L2 entries | 20 | Complete-circuit or chain-level end-to-end flows. |
| Release task forms | 269 | Materialized `dut`, `tb`, `bugfix`, and/or `e2e` forms. |
| Strong content-denominator entries | 75 | Package entries allowed to support distinct-function benchmark claims after duplicate L2 exclusions. |
| Strong content-denominator forms | 259 | Materialized forms attached to the 75 included entries. |
| Content-excluded entries/forms | 5 / 10 | Duplicate L2 package assets retained as evidence only pending rewrite. |
| Certified forms | 269 | Forms with static, EVAS, and Spectre certification evidence. |
| Pending forms | 0 | Forms still lacking release certification. |
| EVAS PASS / Spectre FAIL | 0 | Hard parity mismatch count. |
| Scored entries/forms | 0 / 0 | Scoring remains disabled by policy. |

The latest full release dual rerun completed with `164/164` primary rows
passing EVAS/Spectre and `expected_miss_count=0`.

## Content Denominator Exclusions

These entries remain in the package as traceable assets, but they must not be
counted as distinct L2 benchmark functions or denominator rows until rewritten.

| Excluded entry | Kept canonical entry | Reason |
| --- | --- | --- |
| `vbr1_l2_sar_adc_mini_loop` | `vbr1_l2_adc_dac_source_sweep_flow` | Current gold is an ADC/DAC sweep kernel, not a distinct SAR feedback loop. |
| `vbr1_l2_sample_hold_plus_calibration_system_flow` | `vbr1_l2_adc_dac_source_sweep_flow` | Same normalized ADC/DAC sweep kernel, not a distinct sample/hold system flow. |
| `vbr1_l2_source_driven_verification_flow` | `vbr1_l2_adc_dac_source_sweep_flow` | Same normalized ADC/DAC sweep kernel, not a distinct source-driven flow. |
| `vbr1_l2_signal_conditioning_chain` | `vbr1_l2_amplifier_filter_chain` | Same normalized gain/filter/hysteresis chain. |
| `vbr1_l2_gain_calibration_convergence_loop` | `vbr1_l2_complete_calibration_loop` | Same normalized calibration loop kernel. |

## Form Counts

| Form | Count | Scope |
| --- | ---: | --- |
| `e2e` | 80 | Every release entry has an end-to-end form. |
| `tb` | 80 | Every release entry has a testbench-generation form. |
| `dut` | 57 | L1 model-capability entries where a standalone DUT form is meaningful. |
| `bugfix` | 52 | L1 entries with a curated buggy/fixed repair surface. |

L2 entries generally use `e2e` and `tb` forms only. Some measurement and source
entries also omit `bugfix` when a fair buggy/fixed repair problem is not yet a
good public benchmark surface.

## Category Summary

| Category | Entries | L1 | L2 | Forms |
| --- | ---: | ---: | ---: | ---: |
| Data Converters | 12 | 8 | 4 | 40 |
| PLL / Clock / Event Timing | 13 | 10 | 3 | 46 |
| Analog Behavioral Signal Conditioning | 11 | 9 | 2 | 40 |
| Calibration, DEM, and Control | 10 | 8 | 2 | 36 |
| Comparators and Decision Circuits | 8 | 7 | 1 | 30 |
| Digital and Event-Driven Logic | 8 | 6 | 2 | 28 |
| Measurement and Testbench Instrumentation | 7 | 5 | 2 | 17 |
| Stimulus and Sources | 6 | 4 | 2 | 16 |
| Sample, Hold, and Analog Memory | 5 | 3 | 2 | 16 |

## Completed Functions By Category

### Data Converters

| Level | Function | Forms |
| --- | --- | --- |
| L1 | Simple 4-bit binary-coded DAC | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Capacitive/weighted SAR feedback DAC | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Clocked ADC quantizer | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | DAC mismatch/unit-weighting model | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | SAR logic | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Segmented DAC | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Thermometer-code decoder | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Unit-element thermometer DAC | `dut`, `tb`, `bugfix`, `e2e` |
| L2 | ADC/DAC reconstruction chain | `tb`, `e2e` |
| L2 | Flash ADC mini-array | `tb`, `e2e` |
| L2 | SAR ADC mini-loop | `e2e`, `tb` content-excluded pending rewrite |
| L2 | Weighted SAR ADC/DAC loop | `tb`, `e2e` |

### PLL / Clock / Event Timing

| Level | Function | Forms |
| --- | --- | --- |
| L1 | Bang-bang phase detector | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Voltage-domain charge-pump control abstraction | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Clock divider | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Digital phase accumulator with modulo wrap | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Lock detector | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Sampled loop-filter abstraction | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | PFD small phase-error response | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | PFD UP/DN logic | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | VCO phase integrator | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | XOR phase detector | `dut`, `tb`, `bugfix`, `e2e` |
| L2 | ADPLL lock/ratio-hop/timer flow | `tb`, `e2e` |
| L2 | CPPLL tracking and frequency-step reacquire flow | `tb`, `e2e` |
| L2 | PLL timing slice | `tb`, `e2e` |

### Analog Behavioral Signal Conditioning

| Level | Function | Forms |
| --- | --- | --- |
| L1 | First-order lowpass | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Higher-order filter | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Resettable integrator | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Slew-rate limiter | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Soft/hysteretic limiter | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Voltage gain amplifier | `dut`, `tb`, `bugfix`, `e2e` |
| L2 | Amplifier/filter chain | `e2e`, `tb` |

### Calibration, DEM, and Control

| Level | Function | Forms |
| --- | --- | --- |
| L1 | Calibration deadband controller | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | DWA/DEM encoder | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Element shuffler | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Gain trim controller | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Rotating DEM selector | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Successive-approximation calibration/search FSM | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Trim-voltage generator | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Windowed DEM pointer | `dut`, `tb`, `bugfix`, `e2e` |
| L2 | Complete calibration loop | `e2e`, `tb` |
| L2 | Gain calibration/convergence loop | `e2e`, `tb` content-excluded pending rewrite |

### Comparators and Decision Circuits

| Level | Function | Forms |
| --- | --- | --- |
| L1 | Hysteresis comparator | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Offset comparator | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Propagation-delay comparator | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | StrongARM-style latch comparator | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Threshold comparator | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Window comparator/detector | `dut`, `tb`, `bugfix`, `e2e` |
| L2 | Single-ramp comparator offset measurement flow | `tb`, `e2e` |

### Digital and Event-Driven Logic

| Level | Function | Forms |
| --- | --- | --- |
| L1 | Debounce latch | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Edge detector | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Retriggerable one-shot pulse stretcher | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | LFSR/PRBS generator | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | One-shot timer | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Serializer/frame aligner | `dut`, `tb`, `bugfix`, `e2e` |
| L2 | Event controller | `tb`, `e2e` |
| L2 | Serializer frame-alignment flow | `tb`, `e2e` |

### Measurement and Testbench Instrumentation

| Level | Function | Forms |
| --- | --- | --- |
| L1 | Crossing metric writer | `tb`, `dut`, `e2e` |
| L1 | Edge interval timer | `tb`, `e2e` |
| L1 | Gain estimator | `tb`, `e2e` |
| L1 | Peak detector | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Settling response measurement helper | `tb`, `e2e` |
| L2 | Gain extraction/convergence measurement flow | `tb`, `e2e` |
| L2 | Measurement flow | `tb`, `e2e` |

### Stimulus and Sources

| Level | Function | Forms |
| --- | --- | --- |
| L1 | Burst clock source | `dut`, `tb`, `e2e` |
| L1 | Dither or noise-like deterministic source | `dut`, `tb`, `e2e` |
| L1 | Periodic phase-ramp guard source | `dut`, `tb`, `e2e` |
| L1 | Sine/periodic voltage source | `dut`, `tb`, `e2e` |
| L2 | ADC/DAC source sweep flow | `e2e`, `tb` |
| L2 | Source-driven verification flow | `e2e`, `tb` content-excluded pending rewrite |

### Sample, Hold, and Analog Memory

| Level | Function | Forms |
| --- | --- | --- |
| L1 | Aperture-delay track-and-hold | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Clocked sample-and-hold | `dut`, `tb`, `bugfix`, `e2e` |
| L1 | Sample-and-hold with droop/leakage | `dut`, `tb`, `bugfix`, `e2e` |
| L2 | Converter front-end | `tb`, `e2e` |
| L2 | Sample/hold plus calibration/system flow | `e2e`, `tb` content-excluded pending rewrite |

## Claim Boundary

This content list supports the claim that the release package has materialized
and EVAS/Spectre-certified benchmark tasks for the listed circuit functions.

It does not enable these claims by itself:

- scored benchmark result,
- model baseline result,
- EVAS speedup result,
- L0 conformance counted as benchmark coverage.

Those remain controlled by the dedicated score denominator, baseline, speed,
and conformance reports.

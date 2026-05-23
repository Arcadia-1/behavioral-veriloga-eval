# vaBench Release Completed Benchmark Contents

Date: 2026-05-24

This note records the benchmark contents currently materialized in the clean
`vabench-release-v1` package. The package manifest remains the source of truth
for score and certification state.

## Evidence Sources

- `benchmark-vabench-release-v1/MANIFEST.json`
- `benchmark-vabench-release-v1/reports/release_status.json`
- `benchmark-vabench-release-v1/reports/score_denominator_manifest.json`
- `benchmark-vabench-release-v1/reports/schema_validation.json`

## Completion Snapshot

| Item | Count | Meaning |
| --- | ---: | --- |
| Release entries | 72 | Top-level L1/L2 circuit functions in the release package. |
| L1 entries | 56 | Single-function model-capability tasks. |
| L2 entries | 16 | Complete-circuit or chain-level flows. |
| Release task forms | 245 | Materialized `dut`, `tb`, `bugfix`, and/or `e2e` forms. |
| Content-denominator entries | 72 | Package entries allowed to support distinct-function benchmark claims. |
| Content-denominator forms | 245 | Materialized forms attached to included entries. |
| Certified entries/forms | 68 / 233 | Static, EVAS, and Spectre currently pass. |
| Pending entries/forms | 4 / 12 | Need fresh dual validation before certification. |
| EVAS PASS / Spectre FAIL | 0 | Hard parity mismatch count in current audited release reports. |
| Scored entries/forms | 68 / 233 | Certified rows currently counted by the score denominator. |

## Form Counts

| Form | Count | Scope |
| --- | ---: | --- |
| `dut` | 53 | Materialized release form. |
| `tb` | 72 | Materialized release form. |
| `bugfix` | 48 | Materialized release form. |
| `e2e` | 72 | Materialized release form. |

## Category Summary

| Category | Entries | L1 | L2 | Forms |
| --- | ---: | ---: | ---: | ---: |
| Analog Behavioral Signal Conditioning | 7 | 6 | 1 | 26 |
| Calibration, DEM, and Control | 9 | 8 | 1 | 34 |
| Comparators and Decision Circuits | 8 | 7 | 1 | 30 |
| Data Converters | 18 | 12 | 6 | 60 |
| Measurement and Testbench Instrumentation | 7 | 5 | 2 | 17 |
| PLL / Clock / Event Timing | 13 | 10 | 3 | 46 |
| Sample, Hold, and Analog Memory | 4 | 3 | 1 | 14 |
| Stimulus and Sources | 6 | 5 | 1 | 18 |

## Completed Functions By Category

### Analog Behavioral Signal Conditioning

| Level | Function | Forms | Certification |
| --- | --- | --- | --- |
| L1 | First-order lowpass | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Higher-order filter | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Resettable integrator | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Slew-rate limiter | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Soft/hysteretic limiter | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Voltage gain amplifier | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L2 | Amplifier/filter chain | `tb`, `e2e` | `certified` |

### Calibration, DEM, and Control

| Level | Function | Forms | Certification |
| --- | --- | --- | --- |
| L1 | Calibration deadband controller | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | DWA/DEM encoder | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Element shuffler | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Gain trim controller | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Rotating DEM selector | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Successive-approximation calibration/search FSM | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Trim-voltage generator | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Windowed DEM pointer | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L2 | Complete calibration loop | `tb`, `e2e` | `certified` |

### Comparators and Decision Circuits

| Level | Function | Forms | Certification |
| --- | --- | --- | --- |
| L1 | Comparator debounce latch | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Hysteresis comparator | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Offset comparator | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Propagation-delay comparator | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | StrongARM-style latch comparator | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Threshold comparator | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Window comparator/detector | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L2 | Single-ramp comparator offset measurement flow | `tb`, `e2e` | `certified` |

### Data Converters

| Level | Function | Forms | Certification |
| --- | --- | --- | --- |
| L1 | ADC code capture register | `dut`, `tb`, `bugfix`, `e2e` | `pending` |
| L1 | ADC/readout serializer frame aligner | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Capacitive/weighted SAR feedback DAC | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Clocked ADC quantizer | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | DAC mismatch/unit-weighting model | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Pipeline ADC MDAC stage | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | SAR logic | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Segmented DAC | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Serial readout deserializer | `dut`, `tb`, `bugfix`, `e2e` | `pending` |
| L1 | Simple 4-bit binary-coded DAC | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Thermometer-code decoder | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Unit-element thermometer DAC | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L2 | ADC/DAC reconstruction chain | `tb`, `e2e` | `certified` |
| L2 | Conversion event controller | `tb`, `e2e` | `pending` |
| L2 | Flash ADC mini-array | `tb`, `e2e` | `certified` |
| L2 | Pipeline ADC chain | `tb`, `e2e` | `certified` |
| L2 | Readout frame-monitor flow | `tb`, `e2e` | `pending` |
| L2 | Weighted SAR ADC/DAC loop | `tb`, `e2e` | `certified` |

### Measurement and Testbench Instrumentation

| Level | Function | Forms | Certification |
| --- | --- | --- | --- |
| L1 | Crossing metric writer | `dut`, `tb`, `e2e` | `certified` |
| L1 | Edge interval timer | `tb`, `e2e` | `certified` |
| L1 | Gain estimator | `tb`, `e2e` | `certified` |
| L1 | Peak detector | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Settling response measurement helper | `tb`, `e2e` | `certified` |
| L2 | Gain extraction/convergence measurement flow | `tb`, `e2e` | `certified` |
| L2 | Measurement flow | `tb`, `e2e` | `certified` |

### PLL / Clock / Event Timing

| Level | Function | Forms | Certification |
| --- | --- | --- | --- |
| L1 | Bang-bang phase detector | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Clock divider | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Digital phase accumulator with modulo wrap | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Lock detector | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | PFD UP/DN logic | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | PFD small phase-error response | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Sampled loop-filter abstraction | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | VCO phase integrator | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Voltage-domain charge-pump control abstraction | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | XOR phase detector | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L2 | ADPLL lock/ratio-hop/timer flow | `tb`, `e2e` | `certified` |
| L2 | CPPLL tracking and frequency-step reacquire flow | `tb`, `e2e` | `certified` |
| L2 | PLL timing slice | `tb`, `e2e` | `certified` |

### Sample, Hold, and Analog Memory

| Level | Function | Forms | Certification |
| --- | --- | --- | --- |
| L1 | Aperture-delay track-and-hold | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Clocked sample-and-hold | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Sample-and-hold with droop/leakage | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L2 | Converter front-end | `tb`, `e2e` | `certified` |

### Stimulus and Sources

| Level | Function | Forms | Certification |
| --- | --- | --- | --- |
| L1 | Burst clock source | `dut`, `tb`, `e2e` | `certified` |
| L1 | Dither or noise-like deterministic source | `dut`, `tb`, `e2e` | `certified` |
| L1 | PRBS stimulus/dither generator | `dut`, `tb`, `bugfix`, `e2e` | `certified` |
| L1 | Periodic phase-ramp guard source | `dut`, `tb`, `e2e` | `certified` |
| L1 | Sine/periodic voltage source | `dut`, `tb`, `e2e` | `certified` |
| L2 | ADC/DAC source sweep flow | `tb`, `e2e` | `certified` |

## Claim Boundary

This content list supports navigation and audit of the release package. It does
not by itself enable speedup, model-baseline, or full-release certification claims;
those remain controlled by the dedicated score, speed, baseline, and claim-gate reports.

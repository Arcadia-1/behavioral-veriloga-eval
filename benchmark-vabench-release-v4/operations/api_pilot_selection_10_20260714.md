# V4 API Pilot Selection 10

- Generated: 2026-07-14
- Release: `benchmark-vabench-release-v4/release/tri-form-v4-1200-final`
- Use: run all three forms per family for paired DUT/Testbench/Bugfix comparison.

| Family | Domain | DUT | Testbench | Bugfix | Why |
|---|---|---|---|---|---|
| 010 `010-offset-comparator` | Comparator / decision threshold | `v4-010` | `v4-510` | `v4-1010` | Simple but representative voltage comparator; useful low-complexity anchor. |
| 024 `024-clocked-sample-and-hold` | Sampling circuit | `v4-024` | `v4-524` | `v4-1024` | Core sampled-data behavior with hold/leakage style checks. |
| 055 `055-first-order-sigma-delta-modulator` | Data converter loop | `v4-055` | `v4-555` | `v4-1055` | Converter feedback/sequencing without being an oversized system task. |
| 059 `059-edge-interval-tdc-8b` | TDC / timing measurement | `v4-059` | `v4-559` | `v4-1059` | Timing-to-code behavior and edge interval measurement. |
| 088 `088-cppll-tracking-reacquire-timer` | PLL / lock timing | `v4-088` | `v4-588` | `v4-1088` | PLL-oriented control/timer behavior with reacquisition semantics. |
| 094 `094-iq-downconversion-chain` | RF mixer / IQ chain | `v4-094` | `v4-594` | `v4-1094` | RF/baseband chain coverage beyond converter-heavy tasks. |
| 306 `306-instrumentation-amplifier-offset-trim` | Amplifier + calibration | `v4-306` | `v4-806` | `v4-1306` | Multi-module analog frontend with offset trim behavior. |
| 321 `321-charge-pump-pulse-balancer` | Charge pump / pulse balance | `v4-321` | `v4-821` | `v4-1321` | Charge-pump style pulse balancing and control behavior. |
| 333 `333-image-reject-mixer-calibration-loop` | RF calibration loop | `v4-333` | `v4-833` | `v4-1333` | Calibration loop with mixer/image-rejection semantics. |
| 342 `342-sar-adc-system-4b` | Composed ADC system | `v4-342` | `v4-842` | `v4-1342` | Multi-module system-level SAR ADC anchor for harder cases. |

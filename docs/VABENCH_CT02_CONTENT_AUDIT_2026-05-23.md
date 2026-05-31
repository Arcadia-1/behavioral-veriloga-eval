# CT02 Comparator Content Audit

Date: 2026-05-23

Scope: `benchmark-vabench-release-v1/tasks/CT02_comparator_and_decision_circuits`.

This audit checks whether CT02 prompt/checker content follows the same public-contract direction used for the recent CT01 review: public interface, public observables, behavior-level checks, hidden evaluator boundary, and no hidden checker leakage. It also separates "already certified and acceptable" from "changed in this audit batch and requires fresh EVAS/Spectre dual validation".

## Current Status Matrix

| ID | Release entry | Level | Function | Forms | Current evidence state | Fresh dual needed now |
| --- | --- | --- | --- | --- | --- | --- |
| CT02-01 | `vbr1_l1_threshold_comparator` | L1 | Threshold comparator | `dut`, `tb`, `bugfix`, `e2e` | Fully certified | No |
| CT02-02 | `vbr1_l1_offset_comparator` | L1 | Offset comparator | `dut`, `tb`, `bugfix`, `e2e` | Fully certified | No |
| CT02-03 | `vbr1_l1_propagation_delay_comparator` | L1 | Propagation-delay comparator | `dut`, `tb`, `bugfix`, `e2e` | Fully certified | No |
| CT02-04 | `vbr1_l1_hysteresis_comparator` | L1 | Hysteresis comparator | `dut`, `tb`, `bugfix`, `e2e` | Fully certified | No |
| CT02-05 | `vbr1_l1_strongarm_style_latch_comparator` | L1 | StrongARM-style latch comparator | `dut`, `tb`, `bugfix`, `e2e` | Fully certified | No |
| CT02-06 | `vbr1_l1_window_comparator_detector` | L1 | Window comparator/detector | `dut`, `tb`, `bugfix`, `e2e` | Pending after true-window rewrite | Yes, 4 forms |
| CT02-07 | `vbr1_l2_comparator_measurement_flow` | L2 | Single-ramp comparator offset measurement flow | `tb`, `e2e` | Pending after L2 single-ramp rewrite | Yes, 2 forms |

Total fresh dual queue for CT02 after this audit batch: 6 forms.

## Public-Contract Alignment

| Criterion | CT02 status | Notes |
| --- | --- | --- |
| Public release contract block | Pass | Every current CT02 prompt has the release task contract header and base function metadata. |
| Hidden evaluator boundary | Pass | Prompts explicitly say the deterministic checker and EVAS/Spectre validation are external. |
| Public interface | Pass for forms that generate a DUT | `dut` and `e2e` prompts expose module name, port names, and electrical discipline. `tb` and `bugfix` forms focus on supplied artifacts and observables. |
| Public observables | Pass | Prompts list waveform names the harness/checker expects. |
| Behavior checks | Mixed strength | All prompts expose public behavior checks, but CT02-01 is intentionally basic, while CT02-03/04/06/07 are stronger function-level checks. |
| Gold/checker leakage | Acceptable | Prompts expose behavior names and observable contracts, not hidden checker code. Some exact sample sequences are public because the benchmark task intentionally fixes the stimulus schedule. |
| CT01-style specificity | Partial | CT02-06 and CT02-07 match the newer CT01 style most closely. Some older certified tasks still use compact task descriptions and can be tightened later if desired. |

## Detailed Circuit Audit

| ID | Prompt content and observables | Checker behavior | Coverage strength | Gaps / risk | Recommendation |
| --- | --- | --- | --- | --- | --- |
| CT02-01 Threshold comparator | Public task asks for module `comparator` with `VDD`, `VSS`, `VINP`, `VINN`, `OUT_P`. It describes differential comparison, rail-referenced output, finite output transition, and visible threshold crossing. Public checks include high when `VINP > VINN`, low when `VINP < VINN`, and input-order flip behavior. | `check_comparator` requires `vinp`, `vinn`, `out_p`; rejects stuck output; checks output is mostly high when `vinp > vinn + 20mV` and mostly low when `vinn > vinp + 20mV`. | Basic L1 polarity and non-stuck comparator behavior. | It does not measure exact trip voltage, transition time, output rail accuracy, or small-signal boundary behavior near zero differential. This is acceptable for a simple threshold comparator but weaker than CT01's recent full-code coverage style. | Keep for now. Optional P2 tightening: add explicit below/near/above threshold phases and public rail/timing bounds, then rerun 4 forms if changed. |
| CT02-02 Offset comparator | Public task asks for clocked comparator `cmp_offset_ref` with input offset. It exposes clocked comparison of `VINP - VINN` against a positive offset threshold, rail-level output, smoothed transitions, and saved clock/differential input/output observables. Public checks include sequence `LHHHLLL` and borderline offset decisions. | `check_offset_comparator` samples `out_p` at fixed times and requires decision sequence `LHHHLLL`. The bugfix form also checks low/high clock phases and positive-offset polarity. | Good for deterministic clocked offset behavior under a fixed stimulus schedule. | The main stable checker mostly checks output sequence, not directly reconstructing `VINP - VINN - offset` at each sample. The prompt does expose the intended offset relation, so this is not a leakage problem, but checker strength could be improved. | Keep for now. Optional P2 tightening: checker can compare sampled `VINP`, `VINN`, and declared offset windows instead of relying mainly on sequence. |
| CT02-03 Propagation-delay comparator | Public task asks for `cmp_delay` with clock, differential input, complementary outputs, and four positive-polarity phases whose differential magnitude shrinks from `10mV` to `0.01mV`. It requires all phases to resolve high and delay to grow as the input differential shrinks. | `check_cmp_delay` requires `time`, `clk`, `vinp`, `vinn`, `out_p`; finds output crossing after each clock edge and checks monotonic increase of delay across the four shrinking-differential phases. | Strong L1 functional check for delay-vs-overdrive trend. | It focuses on positive-polarity phases only. It does not check negative-polarity delay symmetry or complementary `out_n` in the primary checker path. | Accept as CT02 L1. Optional future expansion: add negative-polarity phases if we want a stronger comparator-delay benchmark. |
| CT02-04 Hysteresis comparator | Public task asks for `cmp_hysteresis` with `vhys`, separate rising/falling thresholds, state retention inside the hysteresis window, two directional `cross()` events, and saved `vinp`, `vinn`, `out_p`, `out_n`. | `check_cmp_hysteresis` requires `time`, `out_p`, `out_n`; rejects non-toggling outputs; checks low/high/low windows and expected rising/falling trip timing. | Strong enough for L1 hysteresis: it tests memory-like separated trip points through the supplied waveform. | Checker relies on fixed expected timing windows from the reference stimulus rather than deriving thresholds from `vinp-vinn` directly. This is acceptable but less transparent than a waveform-derived threshold checker. | Keep. Optional P2 tightening: derive rising/falling differential trip points from waveform columns and compare against `vhys/2`. |
| CT02-05 StrongARM-style latch comparator | Public task asks for `cmp_strongarm` with clocked evaluate/reset behavior, complementary outputs, positive decisions followed by negative decisions, and saved clock/input/output waveforms. Bugfix focuses on reset priority. | Stable checker samples `out_p/out_n` at 0.75, 1.75, 2.75, 3.75 ns and expects `PPNN`; bugfix checker checks reset window forces both outputs low and active windows match input polarity. | Good for latch-like evaluate/reset sequence and complementary output behavior. | The main checker does not inspect `CLK`, `VINP`, or `VINN` directly; it trusts the fixed testbench schedule and output sample sequence. This is common for deterministic latch tasks but weaker for general comparator reasoning. | Keep. Optional P2 tightening: require sampled `CLK`, `VINP`, `VINN` consistency in the checker if we want stronger public evidence. |
| CT02-06 Window comparator/detector | Public task now explicitly defines a true window comparator: `out` high only for `vlow < vin < vhigh`, low below lower threshold and above upper threshold. It requires a triangular PWL stimulus that sweeps below, inside, above, and back through the window. | `check_true_window_comparator` requires `time`, `vin`, `out`; rejects stuck output; checks below-lower and above-upper windows are low, and inside-window samples are high on both rising and falling sweeps. | Strong L1 true-window behavior; fixes the previous ambiguity with hysteresis/window semantics. | Fresh dual evidence is pending because prompt/gold/checker semantics changed. Current checker uses fixed numeric window bands around 0.3/0.6 V, which matches the prompt. | Keep rewrite. Must run fresh EVAS/Spectre on all 4 forms before paper-facing certification. |
| CT02-07 Single-ramp comparator offset measurement flow | Public task now defines an L2 measurement flow, not a bare comparator: ports include `trip_v`, `offset_est`, and `valid`; `inp` ramps from 0.490 V to 0.520 V with `inn = 0.500 V`; expected trip is near 0.505 V and offset estimate near 0.005 V. | `check_comparator_measurement_flow` requires `time`, `inp`, `inn`, `outp`, `trip_v`, `offset_est`, `valid`; checks pre/post trip output, `valid` assertion, expected trip/offset values, and hold behavior after valid. | Stronger L2 measurement-flow check. It covers comparator decision plus measurement observables. | It is a single-ramp measurement method only. It does not cover closed-loop binary-search offset calibration. This is a deliberate scope choice for CT02; binary search can be a later CT04/control or L2 calibration task. | Keep single-ramp design. Must run fresh EVAS/Spectre on `tb` and `e2e` forms. |

## Audit Judgment

CT02 is structurally aligned with the CT01 prompt cleanup: the prompts expose public contracts and avoid hidden checker code. The only mandatory fresh validation after this audit batch is CT02-06 and CT02-07 because their public behavior/gold/checker contract changed.

The remaining certified CT02 tasks do not have obvious semantic errors, but they are not equally strong:

- CT02-01 is the weakest because it checks broad polarity windows only.
- CT02-02 and CT02-05 rely on fixed output sequences from deterministic stimuli; this is acceptable, but waveform-derived input consistency would be stronger.
- CT02-03, CT02-04, CT02-06, and CT02-07 are better aligned with function-specific behavior checks.

Recommended order:

1. Keep CT02-06 and CT02-07 as the current required rerun set.
2. Before launching a full CT02 rerun, decide whether to upgrade CT02-01, CT02-02, or CT02-05 from "acceptable" to "stronger checker" quality.
3. If no further CT02 prompt/checker changes are made, run fresh EVAS/Spectre dual validation for the current 6 pending forms only.

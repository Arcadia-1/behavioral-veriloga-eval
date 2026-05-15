# Fixed-Only Bugfix Reconstruction Review

Date: 2026-05-15

Scope: the original 18 `family=bugfix` rows in
`docs/VABENCH_MAIN120_MATERIALIZATION.csv` with
`provenance_status=historical_bugfix_fixed_only` and `missing_buggy_fixed_pair`
in `promotion_blockers`.

Conclusion: these rows should not be presented as true bugfix tasks from the
historical fixed-only evidence alone. Each row has fixed staged
source/testbench evidence, but no historical buggy source. A B1 badcase may be
designed for some functions, but it is new reconstruction work and must be
validated as fixed-pass/buggy-fail before claiming bugfix status. As of
2026-05-15, `leaky_hold`, `one_shot_timer`, and `track_hold_aperture` have
source-controlled reconstructed badcases with local EVAS fixed-pass/buggy-fail
evidence; Spectre dual remains pending for those three.

This is a release-form decision, not a value judgment on the underlying
functions. A fixed-only historical `*_bugfix` row may still become useful
benchmark coverage as `spec-to-va`, `tb-generation`, or `end-to-end` when the
public task is reframed around normal implementation/measurement behavior. It
just must not be counted as bugfix capability without a validated badcase.

| task_id | Core function | B1 reconstructable? | Suggested badcase if pursued | Conformance / measurement? | Risk |
|---|---|---:|---|---|---|
| `vbm1_file_metric_writer_bugfix` | Threshold-cross file metric writer with done/valid output. | No from current evidence | Missed first crossing or repeated write when the threshold is crossed multiple times. | Measurement | Medium: file side effects make EVAS/Spectre parity brittle. |
| `vbm1_first_order_lowpass_bugfix` | First-order low-pass state update. | No from current evidence | Wrong update step or stale state around timer/sample boundaries. | Conformance | Low: plausible diagnostic regression, weak as product bugfix without buggy source. |
| `vbm1_gain_trim_controller_bugfix` | Clocked gain-trim calibration controller. | No from current evidence | Reset/edge ordering causes trim update to occur one cycle early/late. | Conformance | Medium: state sequencing can be real, but root cause is speculative. |
| `vbm1_leaky_hold_bugfix` | Sample/hold with leakage decay. | Yes, reconstructed 2026-05-15 | Buggy source omits the leakage decay multiply, so the held level does not decay before reset. | Functional bugfix plus separate decay conformance watch; EVAS/Spectre fixed-pass and buggy-fail confirmed. | Medium: exact timer/startup semantics still belong in conformance. |
| `vbm1_lock_detector_bugfix` | PLL lock detector state machine. | No from current evidence | Off-by-one lock assertion after the required number of aligned cycles. | Conformance | Medium: easy to overfit checker windows. |
| `vbm1_offset_calibration_fsm_bugfix` | Offset calibration FSM and trim code control. | No from current evidence | Startup/reset transition mishandles accumulator clamp or trim direction. | Conformance | Medium: multi-state behavior makes single-root-cause isolation necessary. |
| `vbm1_offset_comparator_bugfix` | Comparator offset reference/characterization. | No from current evidence | Wrong offset threshold or polarity near the crossing point. | Conformance | Medium: may be better as comparator spec/conformance than bugfix. |
| `vbm1_one_shot_timer_bugfix` | One-shot pulse generator with reset/retrigger behavior. | Yes, reconstructed 2026-05-15 | Buggy source omits reset falling-edge clear, so an active pulse persists until timeout. | Functional bugfix plus separate timer-boundary conformance watch; EVAS/Spectre fixed-pass and buggy-fail confirmed. | Medium-high: exact timeout boundary still belongs in conformance. |
| `vbm1_peak_detector_bugfix` | Peak detector with reset. | No from current evidence | Peak register fails to reset or misses a later higher peak. | Conformance | Low: plausible but unproven badcase. |
| `vbm1_precision_rectifier_bugfix` | Precision rectifier output shaping. | No from current evidence | Negative input branch leaks below zero or sign crossing saturates incorrectly. | Conformance | Low: likely normal spec coverage unless a buggy source is reconstructed. |
| `vbm1_resettable_counter_divider_bugfix` | Resettable divider and reference divider pair. | No from current evidence | Reset release causes divider phase/count off by one. | Conformance | High: staged fixture includes DUT and ref model, so reconstruction risks mixing harness parity with DUT defect. |
| `vbm1_resettable_integrator_bugfix` | Resettable analog integrator. | No from current evidence | Integration continues during reset or restarts from stale state. | Conformance | Medium: overlaps unsupported/fragile analog-state semantics. |
| `vbm1_sar_logic_4b_bugfix` | 4-bit SAR control sequence. | No from current evidence | Ready/EOC asserted one clock early/late or bit trial order reversed. | Conformance | High: SAR sequencing has many plausible bugs; badcase must isolate one. |
| `vbm1_settling_time_measurement_tb_bugfix` | Settling-time measurement helper/testbench logic. | No from current evidence | Done condition tied to a brittle time/value threshold. | Measurement | Medium: should likely be measurement/conformance, not model-capability bugfix. |
| `vbm1_slew_rate_limiter_bugfix` | Slew-rate limiter. | No from current evidence | Large input step overshoots allowed slew slope for one update. | Conformance | Low-medium: plausible but still reconstructed. |
| `vbm1_track_hold_aperture_bugfix` | Track/hold aperture timing model. | Yes, reconstructed 2026-05-15 | Buggy source samples immediately at the clock edge instead of after `taperture`. | Functional bugfix plus separate aperture-boundary conformance watch; EVAS/Spectre fixed-pass and buggy-fail confirmed. | Medium: checker must stay on safe post-aperture windows. |
| `vbm1_vco_phase_integrator_bugfix` | VCO phase accumulator and output clock. | No from current evidence | Phase wrap double-toggles or misses a toggle. | Conformance | Medium-high: phase/event scheduling can be simulator-sensitive. |
| `vbm1_voltage_clamp_bugfix` | Voltage clamp/saturation transfer. | No from current evidence | Rail comparison uses wrong bound or fails to saturate at `vlo`/`vhi`. | Conformance | Medium: easy to create a clean badcase, but not evidenced by current fixed-only row. |

Inspected evidence pattern:
- CSV rows: `docs/VABENCH_MAIN120_MATERIALIZATION.csv`.
- EVAS staged roots: `results/vabench-main-v1-main120-gold-evas-2026-05-08/<task_id>/staged/`.
- Spectre staged roots: `results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08/<task_id>/staged/`.
- For all 18 rows, staged source files matched between EVAS and Spectre and only fixed/reference material was present.

Recommended handling:
- Mark these as fixed-only evidence or conformance/measurement candidates in any release-facing table.
- Reuse the underlying function as `spec-to-va`, `tb-generation`, or `end-to-end` only after writing reviewed `prompt.md`, `meta.json`, `checks.yaml`, and gold assets for that non-bugfix family.
- Promote to true bugfix only after adding `dut_buggy.va`, `dut_fixed.va`, targeted badcase testbench, public checks, and fresh fixed-pass/buggy-fail EVAS/Spectre evidence.

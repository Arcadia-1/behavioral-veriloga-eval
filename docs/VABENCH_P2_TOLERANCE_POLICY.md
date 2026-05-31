# vaBench P2 Tolerance and Watchlist Policy

Date: 2026-05-14

## Scope

This policy covers PASS/PASS EVAS/Spectre drift classes from `EVAS_SPECTRE_PASS_DRIFT_AUDIT.md` that are currently classified as `P2-checker`, `P2-tolerance`, or `P2-watch`.

P2 means both backends pass the public checker and the current evidence looks like simulator sampling or bounded numeric drift, not an EVAS kernel bug. P2 does not mean exact waveform or note equality is required.

## Default Rules

- Do not use raw saved-row fractions such as `high rows / total rows` as primary benchmark metrics.
- Prefer behavior contracts that survive accepted-point grid differences: edge counts, event ordering, state classification, decision samples, time-weighted durations, and windowed voltage means.
- Keep binary semantics exact where possible: pulse counts, reset state, overlap/no-overlap classification, sign/trend direction, and pass/fail classification should match.
- Treat numeric tolerances as bounded acceptance bands around public behavior, not as permission to hide binary behavior changes.
- Promote a P2 case to P0/P1 investigation when a drift changes binary classification, changes edge/pulse counts, flips reset or decision polarity, violates monotonic/trend expectations, or repeats across related kernels with increasing magnitude.
- Sampling helpers used by release checks must reject out-of-range sample times
  instead of extrapolating from the first or last saved row.

## Policy Table

| P2 class | Representative tasks | Robust metric | Default tolerance | Escalate to P0/P1 when |
| --- | --- | --- | --- | --- |
| `time_fraction_sampling_drift` | `edge_detector`, `one_shot_timer`, `lock_detector` | Rising/falling edge counts, event order, first/last edge time, time-weighted high duration or late-lock duration. | Edge and state counts exact. Timing windows use the larger of 1 ns or 5% of the expected pulse/window duration. Duty/fraction summaries may be reported only as secondary diagnostics with an absolute fraction tolerance of 0.05. | Edge count changes, missing trigger/lock event, event order changes, late-lock classification flips, or time-weighted duration falls outside tolerance. |
| `event_timing_quantization_drift` | `pfd_reset_race` | UP/DN pulse counts, UP-before-DN or DN-before-UP classification, no-overlap classification, time-weighted pulse duration per phase window. | Pulse counts and overlap classification exact. Timing fractions use absolute fraction tolerance 0.002 or 1 ns equivalent, whichever is stricter for the declared window. | UP/DN pulse counts diverge, overlap becomes nonzero beyond tolerance, first/second phase classification flips, or timing drift grows across related PFD/reset cases. |
| `continuous_response_numeric_drift` | `first_order_lowpass` | Windowed voltage mean/sample at declared times plus monotonic/trend assertions. | Voltage absolute tolerance 5 mV for main120-style 0-1 V behavior, with trend/settling direction exact. This covers the observed about 1 mV lowpass drift with margin. | Final/late window exits tolerance, monotonic direction fails, settling state classification changes, or similar response drift appears across multiple continuous-response kernels. |
| `continuous_decay_numeric_drift` | `leaky_hold` | Hold level, decay direction, reset recovery level, and windowed voltage means during hold/decay/reset windows. | Voltage absolute tolerance 10 mV for decay/hold windows and 5 mV for reset-near-zero windows. Keep this class on the watchlist because it is related to `$abstime` decay semantics. | Hold/decay/reset classification changes, reset does not recover near zero, decay direction is wrong, tolerance is exceeded, or `$abstime` decay conformance regresses. |
| `continuous_integration_numeric_drift` | `resettable_integrator` | Reset level, integration sign, ordered window means across integration phases, post-reset recovery window. | Voltage absolute tolerance 10 mV for integration window means and 5 mV for reset-near-zero checks. This covers observed few-mV integration drift with margin. | Reset classification changes, integration sign/trend flips, window ordering fails, tolerance is exceeded, or future candidates flip pass/fail on integrator behavior. |
| `comparator_reset_window_numeric_drift` | `strongarm_comparator_behavior` bugfix form | Reset-window max, fixed decision sample classification, high/low output window classification. | Reset-window max <= 5 mV unless the task declares a larger noise floor; decision polarity and output classification exact. | Reset max exceeds tolerance, fixed decision samples change polarity, low/high output state classification changes, or bugfix-only drift appears in DUT/TB/E2E forms. |

## Representative Evidence

Current audit evidence is from the 2026-05-08 EVAS and Spectre main120 roots summarized by `EVAS_SPECTRE_PASS_DRIFT_AUDIT.md`.

| Task | Audit classification | Observed note drift | Policy decision |
| --- | --- | --- | --- |
| `vbm1_edge_detector` | `P2-checker` / `time_fraction_sampling_drift` | `high_frac` 0.159 vs 0.141, pulse edges both 4. | Replace row fraction with edge count plus time-weighted pulse duration. |
| `vbm1_one_shot_timer` | `P2-checker` / `time_fraction_sampling_drift` | `pulse_frac` 0.1517 vs 0.1519, trigger and pulse edges both 5. | Keep edge counts exact; allow tiny timing-grid drift in pulse duration. |
| `vbm1_lock_detector` | `P2-checker` / `time_fraction_sampling_drift` | `late_high` 0.789 vs 0.753. | Use lock edge time or time-weighted late-lock duration, not row fraction. |
| `vbm1_pfd_reset_race` | `P2-tolerance` / `event_timing_quantization_drift` | Timing fractions differ by up to 0.0002; pulse counts and overlap classification match. | Keep timing tolerance; escalate only on pulse count or overlap classification divergence. |
| `vbm1_first_order_lowpass` | `P2-tolerance` / `continuous_response_numeric_drift` | Early value differs by about 1 mV; late value matches to three decimals. | Use 5 mV voltage tolerance with trend assertions. |
| `vbm1_leaky_hold` | `P2-watch` / `continuous_decay_numeric_drift` | Hold/decay values differ by up to about 4 mV; reset is 0. | Use 10 mV decay tolerance and keep `$abstime` decay conformance on the watchlist. |
| `vbm1_resettable_integrator` | `P2-tolerance` / `continuous_integration_numeric_drift` | Window means differ by about 3 mV. | Use reset/trend contracts plus 10 mV integration-window tolerance. |
| `vbm1_strongarm_comparator_behavior` bugfix | `P2-tolerance` / `comparator_reset_window_numeric_drift` | Low output windows differ by about 1 mV; reset and high windows match. | Keep reset-window tolerance; decision polarity remains exact. |

## Watchlist

- `continuous_decay_numeric_drift` remains the highest-priority P2 watch class because it is adjacent to `$abstime` decay behavior.
- Any P2 drift that appears in a new task family should be recorded in the drift audit before being accepted as covered by this policy.
- Any P2 drift that causes EVAS `PASS` with Spectre `FAIL` is not P2; it becomes an immediate parity blocker.

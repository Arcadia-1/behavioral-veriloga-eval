# vaBench Main Coverage Table

**Date**: 2026-05-08

This file freezes the first benchmark-expansion target after the bpack48 semantic
audit.  The recommended first paper-facing benchmark is `vaBench-main-v1` with
30 concrete circuit-function packs x 4 forms = 120 tasks.  A separate
`vaBench-heldout-v1` contains 12 unseen packs x 4 forms = 48 tasks.

## Size Decision

| Candidate | Size | Decision | Reason |
| --- | ---: | --- | --- |
| `vaBench-main-120` | 30 packs x 4 forms | Use for v1 | Large enough for first paper-facing matrix; realistic to author, gold-validate, and Spectre-audit. |
| `vaBench-main-192` | 48 packs x 4 forms | Defer to v2 | Stronger statistics, but too much benchmark churn before the protocol is proven. |
| `vaBench-heldout-48` | 12 packs x 4 forms | Required | Prevents skill/RAG/controller overfitting to dev/main. |

Current `bpack48` remains `vaBench-dev48`, not part of the main/heldout score.
It is used for provider smoke, runner debugging, and fast method iteration.

## Split Summary

| Split | Packs | Tasks | Status |
| --- | ---: | ---: | --- |
| `vaBench-dev48` | 12 | 48 | Materialized as `benchmark-bpack-v1`; semantic audit has no hard FAIL after DWA prompt cleanup. |
| `vaBench-main-v1` | 30 | 120 | Materialized as `benchmark-vabench-main-v1`; semantic/integrity/EVAS/Spectre gold gates pass by composed evidence. |
| `vaBench-heldout-v1` | 12 | 48 | Coverage frozen here; must remain unseen for skill/RAG/controller promotion. |

## Existing Dev Packs

| Pack | Mechanism family | Notes |
| --- | --- | --- |
| `threshold_detector` | threshold/static nonlinear | Existing dev pack. |
| `window_detector` | threshold/static nonlinear | Existing dev pack. |
| `analog_limiter` | threshold/static nonlinear | Existing dev pack. |
| `pulse_stretcher` | event/timing | Existing dev pack. |
| `sample_hold` | stateful analog memory | Existing dev pack. |
| `pfd_updn` | event/timing | Existing dev pack. |
| `binary_dac_4b` | data conversion | Existing dev pack. |
| `clock_divider` | mixed-signal timing | Existing dev pack. |
| `hysteresis_comparator` | stateful threshold | Existing dev pack. |
| `flash_adc_3b` | data conversion | Existing dev pack. |
| `dwa_pointer` | pointer/selection | Existing dev pack. |
| `prbs7_lfsr` | mixed-signal protocol | Existing dev pack. |

## vaBench-main-v1 Packs

| Pack | Mechanism family | Source hint | Why include |
| --- | --- | --- | --- |
| `offset_comparator` | threshold/static nonlinear | balanced/comparator | Offset threshold and polarity errors. |
| `strongarm_comparator_behavior` | threshold/static nonlinear | new/public analog behavior | Comparator with clocked decision abstraction. |
| `voltage_clamp` | threshold/static nonlinear | new | Saturating transfer with upper/lower clamps. |
| `precision_rectifier` | threshold/static nonlinear | new | Piecewise sign-dependent analog behavior. |
| `peak_detector` | stateful analog memory | new | Holds historical maximum with reset/leak variants. |
| `track_hold_aperture` | stateful analog memory | balanced/sample-hold variants | Aperture timing beyond simple sample-hold. |
| `debounce_latch` | stateful analog memory | new | State retention under noisy threshold crossings. |
| `leaky_hold` | stateful analog memory | new | Memory plus controlled decay. |
| `edge_detector` | event/timing | benchmark-v2 event family | Short pulse from rising/falling edge. |
| `one_shot_timer` | event/timing | analog-events | Timer/cross interaction and pulse width. |
| `resettable_counter_divider` | event/timing | benchmark-v2 divider_counter | Counter state plus reset phase. |
| `pfd_reset_race` | event/timing | benchmark-v2 pfd_updn_reset_race | Race/mutual exclusion behavior. |
| `thermometer_dac` | data conversion | balanced/data-converter | Code-to-many-element mapping. |
| `segmented_dac` | data conversion | balanced/data-converter | Mixed binary/thermometer structure. |
| `sar_logic_4b` | data conversion | balanced/adc-sar | Sequential conversion decisions. |
| `cdac_calibration` | data conversion/calibration | balanced/adc-sar/dac | Capacitive DAC weight/control behavior. |
| `offset_calibration_fsm` | calibration/control | balanced/calibration | Stateful trim convergence. |
| `gain_trim_controller` | calibration/control | new | Parameter trim and settling. |
| `lock_detector` | calibration/control | balanced/pll-closed-loop | Windowed lock/unlock logic. |
| `background_calibration_accumulator` | calibration/control | new | Slow state update and saturation. |
| `rotating_element_selector` | pointer/selection | benchmark-v2 dwa variants | Generalizes DWA pointer without same task identity. |
| `barrel_pointer_window` | pointer/selection | new | Pointer arithmetic and wraparound windows. |
| `element_shuffler` | pointer/selection | new | Deterministic selection sequence. |
| `thermometer_decoder_guarded` | pointer/selection | benchmark-v2 segment guard | Decoder correctness and glitch guard. |
| `first_order_lowpass` | continuous dynamics | amplifier-filter | Continuous-time filtering. |
| `resettable_integrator` | continuous dynamics | amplifier-filter/new | `idt`-like behavior or equivalent state. |
| `slew_rate_limiter` | continuous dynamics | amplifier-filter/new | Rate-limited output movement. |
| `vco_phase_integrator` | continuous dynamics/pll | pll-clock | Phase accumulation and wrapping. |
| `settling_time_measurement_tb` | source/measurement/TB | measurement/testbench | TB/checker-oriented measurement. |
| `file_metric_writer` | source/measurement/TB | measurement/file IO | `$fopen`/string parameter/Spectre parity stress in normal task form. |

## vaBench-heldout-v1 Packs

| Pack | Mechanism family | Heldout reason |
| --- | --- | --- |
| `folding_adc_encoder` | data conversion | Heldout quantization/encoding family not used in main. |
| `pwm_modulator` | event/timing | Duty-cycle/time encoding generalization. |
| `phase_frequency_lock_monitor` | calibration/control | PLL-like behavior held out from main lock detector. |
| `adaptive_threshold_tracker` | threshold/state | Moving threshold state, not static comparator. |
| `windowed_rms_detector` | continuous dynamics/measurement | Measurement with accumulation/windowing. |
| `charge_pump_behavior` | mixed-signal analog control | Current/voltage abstraction; held out from PFD. |
| `sigma_delta_modulator_1st` | data conversion/dynamics | Feedback quantizer, harder than DAC/ADC mapping. |
| `glitch_filter` | event/timing | Rejects short pulses; complements pulse stretcher. |
| `quadrature_phase_detector` | phase/mixed-signal | Phase relation behavior not in main. |
| `sample_rate_converter_stub` | mixed-signal protocol | Multi-clock event behavior. |
| `temperature_sensor_lut` | source/modeling | Parameterized nonlinear mapping. |
| `noise_source_stat_tb` | source/measurement/TB | Statistical/noise-oriented TB held out from deterministic main. |

## Coverage Counts

| Mechanism family | Main packs | Heldout packs |
| --- | ---: | ---: |
| threshold/static nonlinear | 4 | 1 |
| stateful analog memory | 4 | 1 |
| event/timing | 4 | 3 |
| data conversion | 4 | 2 |
| calibration/control | 4 | 2 |
| pointer/selection | 4 | 0 |
| continuous dynamics | 4 | 1 |
| source/measurement/TB | 2 | 2 |

## Promotion Gates For Each Pack

1. Author all four forms: `bugfix`, `spec-to-va`, `end-to-end`, `tb-generation`.
2. Run semantic prompt-checker-gold audit with zero `FAIL`.
3. Gold passes strict-EVAS.
4. Gold passes Spectre or the pack is withheld from main.
5. No routing or retrieval may use task id, gold code, checker internals, or directory names.
6. Heldout packs are not used to tune compile skills, behavior skills, RAG cards, or controller policies.

## Experiment Gate After Benchmark Freeze

Run A/D/C/S1/S2 on `vaBench-main-v1` only after all promoted packs pass the gates
above.  Behavior-skill, controller, RAG, and SFT/DPO are gated by residual
analysis on main and final validation on heldout.

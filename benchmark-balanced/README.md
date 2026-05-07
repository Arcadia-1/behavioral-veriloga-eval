# Benchmark Balanced

This is the maintained 143-task benchmark for vaEVAS mainline experiments.  It
is organized by task form and circuit-function coverage: every core-function
family has at least one task in each of the four task forms, while individual
tasks avoid duplicate copies of the same observable behavior.

Total tasks: **143**

| task form | count |
|---|---:|
| bugfix | 25 |
| dut-only/spec-to-va | 33 |
| end-to-end | 62 |
| tb-generation | 23 |

The benchmark is task-form covered rather than count-equal: the current task mix
contains more end-to-end tasks than the other forms.  Future additions should be
made as circuit-function packs: add one function family, then cover the relevant
task forms without introducing duplicate observable behaviors.

| core function | count |
|---|---:|
| adc-sar | 8 |
| amplifier-filter | 4 |
| analog-events | 5 |
| analog_limiter | 4 |
| calibration | 5 |
| comms | 4 |
| comparator | 11 |
| dac | 5 |
| data-converter | 10 |
| digital-logic | 19 |
| measurement | 5 |
| phase-detector | 8 |
| pll | 4 |
| pll-clock | 10 |
| pll-closed-loop | 5 |
| pulse_stretcher | 4 |
| sample-hold | 5 |
| signal-source | 5 |
| stimulus | 10 |
| testbench | 4 |
| threshold_detector | 4 |
| window_detector | 4 |

## Four-Form Function Packs

Some core functions are materialized as exact four-form packs.  Each listed
function has one task in each task form:

- end-to-end
- DUT/spec-to-VA (`dut-only`)
- testbench generation
- bugfix

| task id | core function | task form |
|---|---|---|
| `balanced_threshold_detector_e2e` | threshold_detector | end-to-end |
| `balanced_threshold_detector_dut` | threshold_detector | dut-only/spec-to-va |
| `balanced_threshold_detector_tb` | threshold_detector | tb-generation |
| `balanced_threshold_detector_bugfix` | threshold_detector | bugfix |
| `balanced_window_detector_e2e` | window_detector | end-to-end |
| `balanced_window_detector_dut` | window_detector | dut-only/spec-to-va |
| `balanced_window_detector_tb` | window_detector | tb-generation |
| `balanced_window_detector_bugfix` | window_detector | bugfix |
| `balanced_analog_limiter_e2e` | analog_limiter | end-to-end |
| `balanced_analog_limiter_dut` | analog_limiter | dut-only/spec-to-va |
| `balanced_analog_limiter_tb` | analog_limiter | tb-generation |
| `balanced_analog_limiter_bugfix` | analog_limiter | bugfix |
| `balanced_pulse_stretcher_e2e` | pulse_stretcher | end-to-end |
| `balanced_pulse_stretcher_dut` | pulse_stretcher | dut-only/spec-to-va |
| `balanced_pulse_stretcher_tb` | pulse_stretcher | tb-generation |
| `balanced_pulse_stretcher_bugfix` | pulse_stretcher | bugfix |

## Gold Validation

The 16 exact four-form pack gold artifacts were validated on 2026-04-30:

| backend | result |
|---|---:|
| EVAS | 16/16 PASS |
| real Spectre | 16/16 PASS |

An additional four-task smoke sample from the non-pack portion of the benchmark
was also validated:

| backend | result |
|---|---:|
| EVAS | 4/4 PASS |
| real Spectre | 4/4 PASS |

Reproduce the four-form pack validation from `behavioral-veriloga-eval/`:

```bash
python3 runners/materialize_benchmark_balanced_tasks.py
python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-balanced \
  --family benchmark-balanced \
  --backend evas \
  --output-dir results/benchmark-balanced-supplement-gold-evas-2026-04-30-r2 \
  --timeout-s 180 \
  --task balanced_threshold_detector_e2e \
  --task balanced_threshold_detector_dut \
  --task balanced_threshold_detector_tb \
  --task balanced_threshold_detector_bugfix \
  --task balanced_window_detector_e2e \
  --task balanced_window_detector_dut \
  --task balanced_window_detector_tb \
  --task balanced_window_detector_bugfix \
  --task balanced_analog_limiter_e2e \
  --task balanced_analog_limiter_dut \
  --task balanced_analog_limiter_tb \
  --task balanced_analog_limiter_bugfix \
  --task balanced_pulse_stretcher_e2e \
  --task balanced_pulse_stretcher_dut \
  --task balanced_pulse_stretcher_tb \
  --task balanced_pulse_stretcher_bugfix
python3 runners/validate_benchmark_v2_gold.py \
  --bench-dir benchmark-balanced \
  --family benchmark-balanced \
  --backend spectre \
  --output-dir results/benchmark-balanced-supplement-gold-spectre-2026-04-30-r2 \
  --timeout-s 180 \
  --spectre-mode spectre \
  --task balanced_threshold_detector_e2e \
  --task balanced_threshold_detector_dut \
  --task balanced_threshold_detector_tb \
  --task balanced_threshold_detector_bugfix \
  --task balanced_window_detector_e2e \
  --task balanced_window_detector_dut \
  --task balanced_window_detector_tb \
  --task balanced_window_detector_bugfix \
  --task balanced_analog_limiter_e2e \
  --task balanced_analog_limiter_dut \
  --task balanced_analog_limiter_tb \
  --task balanced_analog_limiter_bugfix \
  --task balanced_pulse_stretcher_e2e \
  --task balanced_pulse_stretcher_dut \
  --task balanced_pulse_stretcher_tb \
  --task balanced_pulse_stretcher_bugfix
```

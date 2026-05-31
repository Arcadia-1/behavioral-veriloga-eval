# vaEVAS Speed Ablation Experiment Plan

**Date**: 2026-05-22
**Host target**: `thu-sui`
**Worker budget**: 8 parallel jobs
**Primary slice**: vaBench release speed rows, `--suite all --limit 100000`
**Primary gate**: unchanged same-server Spectre-equivalence gate

**Current canonical location**: this plan and its compact reports now live under
`speed-optimization/`. Older `docs/` and release-report paths are compatibility
symlinks.

## Objective

Turn the current speed observation into a paper-usable claim boundary:

1. Isolate which EVAS speed mechanism matters:
   `profile_fast`, `skip_source_error_control`, or their combination.
2. Verify that speed gains do not break behavior or waveform parity.
3. Separate cold-cache and warm-cache timing before making speed claims.
4. Explain slow outliers with EVAS perf counters, not speculation.

## Current Evidence Baseline

Current full same-server gate-fixed evidence:

| Backend | Mode | Runs | PASS | Total wall s | Geomean wall s |
| --- | --- | ---: | ---: | ---: | ---: |
| EVAS | `profile_fast_skip_source_error_control` | 259 | 259 | 433.987 | 0.934 |
| EVAS | `strict_current` | 259 | 259 | 1459.492 | 1.674 |
| Spectre | `ax` | 259 | 259 | 402.593 | 1.398 |
| Spectre | `classic` | 259 | 259 | 1255.295 | 4.602 |

Spectre-equivalence gate:

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| `profile_fast_skip_source_error_control` | 259 | 259 | 0 | 0 | 0 |
| `strict_current` | 259 | 259 | 0 | 0 | 0 |

Spectre-equivalence-gated geomean speedups:

| Pair | Geomean Spectre / EVAS |
| --- | ---: |
| `spectre/ax` vs `EVAS/profile_fast_skip_source_error_control` | 1.497x |
| `spectre/classic` vs `EVAS/profile_fast_skip_source_error_control` | 4.928x |
| `spectre/ax` vs `EVAS/strict_current` | 0.835x |
| `spectre/classic` vs `EVAS/strict_current` | 2.748x |

Current interpretation:

- Fast+skip is safe under the current gate on this slice.
- Fast+skip is clearly useful versus EVAS strict and Spectre classic.
- Fast+skip is not yet a stable wall-clock win versus Spectre `ax`; repeated
  cold/warm measurements are required.

## Fixed Controls

All experiments must keep these fixed unless explicitly recorded:

| Control | Value |
| --- | --- |
| Host | `thu-sui` |
| Python env | `/home/jinzhihong/venvs/vaevas-speed` |
| Cadence setup | `/home/jinzhihong/TSMC180/setup_cadence_sui.csh` |
| Remote repo | `/home/jinzhihong/vaevas-speed-work-clean/behavioral-veriloga-eval` |
| Jobs | `--jobs 8` |
| Timeout | `--timeout-s 300` initially; raise only for diagnosed timeout rows |
| Suite | `--suite all --limit 100000` |
| Spectre modes | `ax`, `classic` |
| Spectre-equivalence gate | behavior checker + strict EVAS parity + every selected Spectre parity |
| Report policy | write new date-stamped reports; never overwrite previous evidence |

## Claim Map

| Claim | Minimum Convincing Evidence | Blocking Failure |
| --- | --- | --- |
| C1: `profile_fast` reduces EVAS runtime by reducing event refinement. | Full-slice speedup vs `strict_current`, 0 gate failures, perf counters show fewer refined steps. | Any behavior/parity FAIL, or speedup concentrated in only 1-2 rows. |
| C2: `skip_source_error_control` reduces source-edge over-refinement without changing model-visible behavior. | Full-slice speedup vs `strict_current`, 0 gate failures, perf counters show fewer dynamic shrinks / skipped source ratios. | Any event-sensitive row fails parity, especially PFD/PLL/ADC-DAC rows. |
| C3: combined `profile_fast_skip_source_error_control` is the safe promoted fast mode. | Repeated cold/warm same-server runs show stable Spectre-equivalence-gated speedup and 0 gate failures. | Instability across repetitions or any waveform parity regression. |
| C4: speed claim is case-stratified, not universal. | Outlier table explains where EVAS is faster/slower and why. | Aggregate speedup hides systematic slow class. |

## Experiment E0: Preflight Reproducibility

Purpose: verify the remote workdir can reproduce the selected 259-row slice
before spending compute.

Command template:

```bash
cd /home/jinzhihong/vaevas-speed-work-clean/behavioral-veriloga-eval
source /home/jinzhihong/venvs/vaevas-speed/bin/activate
source /home/jinzhihong/TSMC180/setup_cadence_sui.csh

python -m py_compile \
  runners/simulate_evas.py \
  runners/run_gold_dual_suite.py \
  runners/run_vabench_release_same_server_speed.py \
  runners/run_vabench_release_evas_speed_experiment.py

python runners/run_vabench_release_same_server_speed.py \
  --suite all --limit 100000 \
  --audit-fixtures-only \
  --output-root results/speed-preflight-fixtures-20260522 \
  --report-json benchmark-vabench-release-v1/reports/speed_preflight_fixtures_20260522.json \
  --report-md benchmark-vabench-release-v1/reports/speed_preflight_fixtures_20260522.md
```

Success gate:

- `py_compile` passes.
- fixture audit is `259 / 259 PASS`.
- no missing `ahdl_include`, missing testbench, or missing CSV blockers.

## Experiment E1: Full Same-Server Ablation Matrix

Purpose: isolate which acceleration mechanism matters.

Modes:

| Group | EVAS modes | Spectre modes |
| --- | --- | --- |
| Full ablation | `strict_current`, `profile_balanced`, `profile_fast`, `skip_source_error_control`, `profile_fast_skip_source_error_control` | `ax`, `classic` |

Expected backend-mode jobs:

```text
259 rows * (5 EVAS modes + 2 Spectre modes) = 1813 jobs
```

Command template:

```bash
python runners/run_vabench_release_same_server_speed.py \
  --suite all --limit 100000 \
  --evas-mode strict_current \
  --evas-mode profile_balanced \
  --evas-mode profile_fast \
  --evas-mode skip_source_error_control \
  --evas-mode profile_fast_skip_source_error_control \
  --spectre-mode ax \
  --spectre-mode classic \
  --jobs 8 \
  --timeout-s 300 \
  --output-root results/same-server-speed-ablation-full-20260522 \
  --report-json benchmark-vabench-release-v1/reports/same_server_speed_ablation_full_20260522.json \
  --report-md benchmark-vabench-release-v1/reports/same_server_speed_ablation_full_20260522.md
```

Metrics:

- PASS / non-PASS by backend and mode.
- Accuracy gate PASS / FAIL / BLOCKED / missing by EVAS mode.
- Geomean, median, min/max, and slowest-row wall time by mode.
- Geomean speedup for each Spectre mode vs each EVAS mode.
- Per-row speedup distribution and slowest EVAS rows.

Decision gate:

- `profile_fast_skip_source_error_control` must remain `259/259` gate PASS.
- `profile_fast` and `skip_source_error_control` may fail as ablations, but any
  failure must be kept as evidence and not promoted.
- If `profile_balanced` has similar safety with better speed/accuracy tradeoff
  than `profile_fast`, keep it as the conservative fast mode candidate.

## Experiment E2: Repeated Cold-Cache Timing

Purpose: measure timing variance using fresh output roots.

Run count:

```text
N = 5 cold repetitions
```

Modes:

```text
EVAS: strict_current, profile_fast_skip_source_error_control
Spectre: ax, classic
```

Expected jobs:

```text
5 repeats * 259 rows * 4 backend/modes = 5180 jobs
```

Command template for repeat `R`:

```bash
python runners/run_vabench_release_same_server_speed.py \
  --suite all --limit 100000 \
  --evas-mode strict_current \
  --evas-mode profile_fast_skip_source_error_control \
  --spectre-mode ax \
  --spectre-mode classic \
  --jobs 8 \
  --timeout-s 300 \
  --output-root results/same-server-speed-cold-r${R}-20260522 \
  --report-json benchmark-vabench-release-v1/reports/same_server_speed_cold_r${R}_20260522.json \
  --report-md benchmark-vabench-release-v1/reports/same_server_speed_cold_r${R}_20260522.md
```

Success gate:

- Every repeat has `259/259` gate PASS for both EVAS modes.
- Report median and IQR across repeats.
- Do not make a paper speed claim if `spectre/ax` vs fast+skip confidence is
  unstable or changes sign under total wall time.

## Experiment E3: Warm-Cache Timing

Purpose: separate simulator startup / AHDL compilation / filesystem effects
from steady-state transient execution.

Current runner limitation:

- `run_vabench_release_same_server_speed.py` deletes staged/run dirs before
  every run, so a true warm-cache pass needs a small runner option.

Required runner extension:

```text
--cache-policy cold|warm
--repeat N
--warmup-runs K
```

Minimal implementation:

- `cold`: current behavior; fresh output root or cleaned run dirs.
- `warm`: run once as warmup, preserve staged and Spectre run dirs, then time
  the measured pass without deleting them.
- Report both wrapper wall time and Spectre-reported timing from `spectre.out`.

Warm experiment after extension:

```bash
python runners/run_vabench_release_same_server_speed.py \
  --suite all --limit 100000 \
  --evas-mode strict_current \
  --evas-mode profile_fast_skip_source_error_control \
  --spectre-mode ax \
  --spectre-mode classic \
  --jobs 8 \
  --timeout-s 300 \
  --cache-policy warm \
  --warmup-runs 1 \
  --repeat 5 \
  --output-root results/same-server-speed-warm-repeat5-20260522 \
  --report-json benchmark-vabench-release-v1/reports/same_server_speed_warm_repeat5_20260522.json \
  --report-md benchmark-vabench-release-v1/reports/same_server_speed_warm_repeat5_20260522.md
```

Decision gate:

- If warm `spectre/ax` eliminates fast+skip's speedup, the paper claim should be
  framed as `classic` / strict-path speedup only.
- If fast+skip remains stable in warm geomean but not total wall time, report
  both and avoid an absolute universal speedup claim.

## Experiment E4: Slow Outlier Perf-Counter Diagnosis

Purpose: explain why EVAS is still slow on some rows.

Rows:

- Top 20 rows by EVAS fast+skip wall time.
- Top 20 rows where `spectre/ax / EVAS fast+skip < 1`.
- Always include:
  - `vbr1_l2_gain_extraction_convergence_measurement_flow`
  - `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow`
  - `vbr1_l2_pll_timing_slice`
  - `vbr1_l2_weighted_sar_adc_dac_loop`

Perf counters to collect:

```text
steps_total
cross_refine_triggers
cross_event_steps
dynamic_step_shrinks
dynamic_step_grows
source_breakpoint_clamps
model_breakpoint_clamps
bound_step_clamps
output_step_clamps
min_step_clamps
err_ratio_skipped_outputs
err_ratio_skipped_sources
```

Output:

- `benchmark-vabench-release-v1/reports/speed_outlier_perf_counter_20260522.json`
- `benchmark-vabench-release-v1/reports/speed_outlier_perf_counter_20260522.md`

Required analysis table:

| Row | Mode | Wall s | Steps | Cross triggers | Dynamic shrinks | Source clamps | Model clamps | Likely cause |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |

Decision gate:

- A slow class must map to a concrete mechanism:
  dense cross events, transition breakpoints, source breakpoints, `$bound_step`,
  record density, or Python/CSV overhead.

## Experiment E5: Accuracy Stress / Tolerance Sweep

Purpose: prove fast+skip is not passing only because current parity tolerance is
too loose.

No simulation rerun is needed initially. Reuse full-ablation or full-v4 CSVs.

Sweeps:

| Sweep | Values |
| --- | --- |
| waveform absolute tolerance scale | `1.0`, `0.5`, `0.25` |
| edge-time tolerance scale | `1.0`, `0.5`, `0.25` |
| high-risk subset | PFD, PLL, ADC-DAC, gain/measurement flows |

Metrics:

- Gate pass count under stricter tolerances.
- Edge time shift distribution.
- Pulse width error distribution.
- Final code / final metric error for ADC-DAC and measurement flows.

Decision gate:

- If all 259 rows pass at `0.5x` tolerance, claim can say "robust under a
  stricter parity sweep".
- If only high-risk timing rows fail, report the exact failure class and keep
  paper wording conservative.

## Run Order

| Milestone | Runs | Workers | Stop / Go Gate |
| --- | --- | ---: | --- |
| M0 preflight | fixture audit only | 8 | must be 259/259 PASS |
| M1 full ablation | 1813 jobs | 8 | fast+skip must be 259/259 gate PASS |
| M2 cold repeat R1 | 1036 jobs | 8 | compare with current full-v4; if unstable, inspect before R2-R5 |
| M3 cold repeats R2-R5 | 4144 jobs | 8 | summarize median/IQR and per-pair geomean |
| M4 warm runner extension | code + smoke | local + 8 | warm smoke must match cold behavior gates |
| M5 warm repeat5 | 5180 jobs | 8 | report cold/warm split |
| M6 outlier diagnosis | selected rows only | 8 | every slow class has a concrete counter explanation |
| M7 waveform diagnostics | CSV-only first | local | relative/absolute error table produced |

## Paper Claim Decision Rules

Allowed wording if all gates pass:

```text
On the vaBench release slice, the promoted EVAS fast mode preserves the
current behavior/waveform parity gates while reducing EVAS runtime. Against
Spectre classic it provides a stable same-server speed advantage; against
Spectre X/ax, the benefit is case-dependent and should be reported with
cold/warm-cache stratification.
```

Forbidden wording unless repeated warm/cold evidence supports it:

```text
EVAS is always faster than Spectre.
EVAS fast mode is accuracy-free / lossless.
Spectre/ax is slower than EVAS on the full release package.
```

## Goal-Mode Execution Prompt

Use this prompt to launch the execution as a bounded goal:

```text
Goal: produce paper-usable EVAS speed evidence for vaBench release v1 using
8 workers on thu-sui, without weakening any Spectre-equivalence gate.

Context:
- Repo: /Users/bucketsran/Documents/TsingProject/vaEvas
- Remote repo: /home/jinzhihong/vaevas-speed-work-clean/behavioral-veriloga-eval
- Remote venv: /home/jinzhihong/venvs/vaevas-speed
- Cadence setup: /home/jinzhihong/TSMC180/setup_cadence_sui.csh
- Existing gate-fixed full run:
  benchmark-vabench-release-v1/reports/same_server_speed_sui_repro_full_v4_gatefix_20260522.json
- Current gate result: fast+skip and strict are both 259/259 PASS.

Constraints:
- Use --jobs 8 for remote simulation runs.
- Keep the selected slice fixed with --suite all --limit 100000.
- Keep Spectre modes fixed to ax and classic.
- Do not relax behavior checkers or waveform parity thresholds for the main gate.
- Write new date-stamped reports; do not overwrite existing reports.
- Preserve unrelated worktree changes.

Tasks:
1. Run remote preflight: py_compile plus fixture audit for all 259 rows.
2. Run full same-server ablation:
   EVAS modes strict_current, profile_balanced, profile_fast,
   skip_source_error_control, profile_fast_skip_source_error_control;
   Spectre modes ax and classic; jobs=8.
3. Summarize pass/non-pass, Spectre-equivalence gates, per-pair geomean speedups, median,
   min/max row speedups, and slowest rows.
4. If fast+skip is not 259/259 gate PASS, stop speed-claim work and diagnose.
5. Run N=5 cold-cache repeats for strict_current and fast+skip versus Spectre
   ax/classic, jobs=8, with fresh output roots per repeat.
6. Add or use a warm-cache runner option only if needed; then run N=5 warm-cache
   repeats with one warmup pass and preserved run dirs.
7. Generate a slow-outlier perf-counter report for the worst EVAS rows and
   rows where spectre/ax beats fast+skip.
8. Run CSV-only waveform diagnostics using relative RMS error, absolute voltage
   error, and event/digital mismatch checks.
9. Produce a final Markdown report with:
   - claim decision
   - full ablation table
   - cold/warm repeated timing table
   - Spectre-equivalence gate table
   - outlier mechanism table
   - allowed and forbidden paper wording

Success criteria:
- Full ablation report exists locally and remotely.
- Cold repeat summary exists for N=5.
- Warm repeat summary exists or a clear runner limitation is documented.
- Outlier perf-counter report exists.
- Waveform diagnostic report exists.
- No promoted mode has any behavior/parity FAIL.
- Final conclusion states exactly where EVAS is faster, where it is not, and
  what claim is safe for the paper.
```

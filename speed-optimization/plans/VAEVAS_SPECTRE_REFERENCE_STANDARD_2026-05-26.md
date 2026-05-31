# vaEVAS Spectre Reference Standard

Date: 2026-05-26

## Purpose

This document freezes the simulator vocabulary and reference standard before running the next EVAS precision-ranking experiments. The goal is to avoid mixing product names, command-line presets, and paper claims.

## Official Simulator Vocabulary

Cadence Virtuoso/ADE is the design and simulation environment. The actual circuit simulation engines relevant to this work are in the Spectre Simulation Platform and related AMS flows.

| Official name | Official positioning | vaEVAS relevance |
| --- | --- | --- |
| Spectre Circuit Simulator / base Spectre | SPICE-class analog circuit simulation foundation in the Spectre family | Best operational anchor for a conservative non-accelerated reference path. |
| Spectre APS | Accelerated Parallel Simulator, positioned as a faster Spectre-accuracy path | Useful historical/parallel reference, but not the current runner mode unless explicitly invoked. |
| Spectre X Simulator | High-performance, high-capacity SPICE-accurate simulator with smart presets and accuracy/performance balance | Official high-performance Spectre direction; do not assume our `+preset=ax` label is identical to every Spectre X product configuration. |
| Spectre FX / XPS style FastSPICE paths | FastSPICE/high-capacity transistor-level and memory/SoC-oriented flows | Out of current vaEVAS scope unless we intentionally add FastSPICE baselines. |
| Spectre RF Option | RF analyses such as harmonic balance and shooting Newton | Out of current transient behavioral benchmark scope. |
| Spectre AMS Designer | Mixed-signal co-simulation integrating analog/SPICE with digital HDL/RNM via Xcelium | Relevant positioning context for event-driven mixed-signal simulation, but not the current baseline engine. |

Official source pages used for this vocabulary:

- Cadence Spectre Simulation Platform: https://www.cadence.com/zh_TW/home/resources/datasheets/spectre-simulation-platform-ds.html
- Cadence Circuit Simulation: https://www.cadence.com/en_US/home/tools/custom-ic-analog-rf-design/circuit-simulation.html
- Cadence Spectre X Simulator: https://www.cadence.com/en_US/home/tools/custom-ic-analog-rf-design/circuit-simulation/spectre-x-simulator.html
- Cadence Spectre RF Option: https://www.cadence.com/zh_CN/home/resources/datasheets/spectre-rf-option-ds.html
- Cadence Spectre AMS Designer: https://www.cadence.com/en_US/home/tools/custom-ic-analog-rf-design/circuit-simulation/spectre-ams-designer.html

## Operational Labels In This Repository

These labels are what our runner actually executes.

| Repo label | Command-level definition | Claim role |
| --- | --- | --- |
| `spectre/classic` | `spectre -64 <tb.scs> ...` with no runner-added performance preset | Conservative non-AX reference path for this repo. It is not a Cadence product name. |
| `spectre/ax` | Legacy repo label for `spectre -64 <tb.scs> ... +preset=ax +mt` | Keep for backward compatibility with current artifacts; prefer `spectre/ax_speed` or `spectre/ax_normalized` in new experiments. |
| `spectre/ax_speed` | Current `spectre/ax` speed-baseline condition: original staged testbench plus `+preset=ax +mt` | Use only for speed comparison against EVAS fast. |
| `spectre/ax_normalized` | `+preset=ax +mt` plus the same explicit transient tolerances and per-row `maxstep` rule used by the strict reference | Use for precision ranking against the strict reference. |
| `evas/strict_current` | Current strict EVAS configuration | EVAS internal reference for checking fast-profile drift. |
| `evas/profile_fast_skip_source_error_control` | EVAS fast profile plus source-side error-control skip | Primary fast EVAS candidate. |

Do not write "Spectre AX is less accurate" as a premise. The safe statement is:

> Spectre `+preset=ax` is the high-performance Spectre baseline in this experiment. Accuracy is setting-dependent, so precision claims must be measured against a fixed reference condition.

## Current Reference Hierarchy

The paper-facing hierarchy should be:

1. **Final simulator judge for vaBench functional certification**: Spectre pass/fail.
2. **Current speed baseline**: `spectre/ax_speed`, equivalent to the existing runner `spectre/ax` condition with `+preset=ax +mt`.
3. **Current conservative comparison path**: `spectre/classic` as executed with no runner-added preset.
4. **Current EVAS success condition**: EVAS output must be Spectre-equivalent under behavior checks plus waveform acceptance gates.
5. **Future stronger precision claim**: EVAS fast is closer than Spectre ax-mode to a stricter Spectre reference. This is not yet established and requires the plan below.

## Settings-Normalized Comparison Rule

Before comparing precision, the same row must be simulated under a normalized and logged testbench condition. This is stricter than the current speed report.

| Item | Rule |
| --- | --- |
| DUT/testbench/stimulus/save list | Identical final staged assets for all systems in the row. |
| `tran stop` | Identical per row. |
| `maxstep` | Identical per row across precision-ranking systems; preserve the task's explicit `maxstep` in the primary reference. Do not force one global absolute `maxstep` across all tasks. |
| `errpreset` | Explicitly set to the selected reference value for precision-ranking Spectre modes. |
| `reltol/vabstol/iabstol/gmin` | Explicitly set to the selected reference values for precision-ranking Spectre modes. |
| Output conversion | Same PSFASCII-to-CSV path and same waveform comparator. |
| Manifest | Every row must record the final command, final `tran` line, final `simulatorOptions`, source assets, and staged assets. |

This creates two separate comparison lanes:

- **Speed lane**: compare EVAS fast against `spectre/ax_speed` under the current production speed condition.
- **Precision-ranking lane**: compare `spectre/ax_normalized`, `evas/strict_current`, and `evas/profile_fast_skip_source_error_control` against `spectre/reference_strict_primary` under the same per-row step and Spectre tolerance settings.

Do not use the speed lane to claim "more accurate than ax-mode"; do not use the precision-ranking lane alone to claim production speedup.

## Acceptance Standard For Current Speed Claim

Current claim allowed:

> EVAS fast is faster than Spectre ax-mode while preserving Spectre-equivalent behavior on the evaluated supported subset.

Current claim not yet allowed:

> EVAS fast is more accurate than Spectre ax-mode.

The current acceptance gate remains:

| Check | Gate |
| --- | --- |
| Behavior/spec | task behavior checker PASS |
| Event/digital consistency | no unacceptable event/digital mismatch |
| Relative waveform error | `row_mean_relative_rms_error<=0.10 and worst_signal_relative_rms_error<=0.22`, or `row_mean_relative_rms_error<=0.08 and worst_signal_relative_rms_error<=0.25` |
| Absolute voltage error | `max_rmse_v<=0.05` and `max_abs_v<=0.30` |
| Self-consistency anchor | Spectre `+preset=ax` and non-AX Spectre pass the same equivalence lens on the same row set |

## Strict Reference Definition For Next Experiments

The next precision-ranking experiment must create explicit `spectre/reference_strict_primary` and `spectre/ax_normalized` modes. Proposed normalized definition:

| Setting | Proposed value | Rationale |
| --- | --- | --- |
| `spectre/reference_strict_primary` command preset | no `+preset=ax`; no runner-added acceleration preset | Defines the fixed conservative reference waveform. |
| `spectre/ax_normalized` command preset | `+preset=ax +mt` | Tests ax-mode under the same explicit user tolerances and per-row step rule. |
| `errpreset` | `conservative` for both `reference_strict_primary` and `ax_normalized` unless a task already specifies a stricter effective setting | Make the transient comparison condition explicit. |
| `reltol` | `1e-5` for both `reference_strict_primary` and `ax_normalized` unless a task already specifies a stricter value | More conservative than common `1e-4` settings and shared by both Spectre precision-ranking modes. |
| `vabstol` | `1e-8` for both `reference_strict_primary` and `ax_normalized` unless a task already specifies a stricter value | More conservative voltage tolerance and shared by both Spectre precision-ranking modes. |
| `iabstol` | `1e-12` for both modes | Keep conventional current tolerance explicit. |
| `gmin` | `1e-12` for both modes | Keep stable Spectre default-like floor explicit. |
| `maxstep` | preserve existing task `maxstep` and apply the same value to all precision-ranking systems for that row; optional strict pass can halve it for sensitivity | Avoid changing task observability semantics in the primary reference while keeping same-row comparisons fair. |
| Output | same saved signals and same PSFASCII-to-CSV path as current speed runs | Prevent output-format differences from becoming metric differences. |

Two reference levels are useful:

- `reference_strict_primary`: conservative tolerances, preserve existing task `maxstep`.
- `reference_strict_halfstep`: same as primary but halve `maxstep` where explicit; appendix/sensitivity only.
- `ax_normalized`: ax-mode run under the same explicit tolerance and per-row `maxstep` condition as `reference_strict_primary`.

## Current Setting Audit

The release gold `.scs` files are not globally uniform:

- 221 gold `.scs` files under `benchmark-vabench-release-v1/tasks/CT*/**/forms/*/gold/` contain `tran`.
- 25 contain `errpreset=conservative`; 196 do not explicitly set `errpreset`.
- Common explicit `maxstep` values include `500p`, `20p`, `0.5n`, `250p`, `2n`, `50p`, `5n`, `100p`, `10p`, `1n`, `0.1n`, and `5p`.
- 20 contain explicit `simulatorOptions`; 18 use `reltol=1e-4 vabstol=1e-6`, and 2 use `reltol=1e-5 vabstol=1e-8`.

Implication: precision comparisons are meaningful only after we normalize and record same-row tolerances, step rules, save sets, and commands.

## Paper Wording

Current wording:

> EVAS fast is evaluated against a Spectre-equivalence standard. The speed baseline is Spectre run with `+preset=ax +mt`; the conservative comparison path is Spectre without the runner-added AX preset. Because Spectre accuracy depends on simulator options and transient settings, stronger "more accurate than AX" claims are deferred to a fixed-reference precision-ranking experiment.

Future wording only if supported:

> Against a fixed conservative Spectre reference, EVAS fast is both faster than Spectre `+preset=ax` and at least as close to the reference on accepted waveform metrics.

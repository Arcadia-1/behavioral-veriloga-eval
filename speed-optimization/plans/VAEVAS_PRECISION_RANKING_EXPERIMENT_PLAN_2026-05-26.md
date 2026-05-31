# EVAS / Spectre Precision-Ranking Experiment Plan

Date: 2026-05-26

## Claim Map

| Claim | Status | Minimum convincing evidence | Linked blocks |
| --- | --- | --- | --- |
| C1: EVAS fast is faster than Spectre ax-mode while preserving Spectre-equivalent behavior | Already supported on current speed slice | 1036/1036 equivalence-gated PASS plus same-server repeated speedup | B0, B4 |
| C2: EVAS fast is at least as reference-consistent as Spectre ax-mode | Not yet claimable | EVAS fast vs `spectre/reference_strict_primary` has no worse acceptance rate and no worse main waveform metrics than `spectre/ax_normalized` vs the same reference | B0, B1, B2, B3 |
| Anti-claim: speed comes from silently loosening correctness | Must be ruled out | Fast EVAS matches strict reference gates, and fast-vs-strict EVAS drift remains within Spectre self-consistency envelope | B2, B3 |

## Experiment Blocks

### B0: Settings-Normalization Sanity

- Claim tested: the strict reference and normalized ax-mode conditions are actually applied and logged.
- Why this exists: current gold testbenches do not use globally uniform `errpreset`, `reltol`, `vabstol`, or `maxstep`; precision comparisons are not meaningful until same-row settings are normalized.
- Dataset: a 10-row pilot covering DAC/digital/simple source/PFD/PLL/gain-estimator rows.
- Compared systems: `spectre/classic`, `spectre/ax_speed`, `spectre/ax_normalized`, `spectre/reference_strict_primary`.
- Metrics: injected options manifest, Spectre command, behavior PASS, CSV generated, accepted tran steps, wall time.
- Setup details: no EVAS changes; add runner support for normalized Spectre modes and an options-injection audit record.
- Success criterion: all pilot rows produce behavior PASS and a manifest showing the intended options.
- Failure interpretation: if rows fail because strict options changed semantics, fall back to per-task preservation rules and document exceptions.
- Priority: MUST-RUN.

### B1: Spectre Mode Self-Consistency Against Strict Reference

- Claim tested: Spectre ax-mode's distance to strict reference is quantified.
- Why this exists: we cannot say EVAS is more precise than ax-mode until ax-mode is compared to the same reference.
- Dataset: 259-row speed slice, one repeat first; four clean repeats if stable.
- Compared systems: `spectre/ax_normalized` vs `spectre/reference_strict_primary`; optional diagnostic `spectre/classic` vs `spectre/reference_strict_primary`.
- Metrics: behavior PASS, relative RMS, row-mean relative RMS, max RMS voltage error, max point voltage error, event/digital mismatch, compared-signal count.
- Setup details: reuse current self-consistency script, generalized from ax-mode/classic pair to arbitrary Spectre modes.
- Success criterion: produce a table showing ax-mode acceptance fraction and metric distribution against strict reference.
- Failure interpretation: if ax-mode frequently fails the strict reference gate, the paper should call ax-mode a speed baseline, not a precision baseline.
- Priority: MUST-RUN.

### B2: EVAS Strict And Fast Against Strict Reference

- Claim tested: EVAS fast and EVAS strict remain close to strict Spectre reference.
- Why this exists: this is the direct evidence for whether fast EVAS loses precision.
- Dataset: same 259-row speed slice, same row order, same signals, same checkers.
- Compared systems: `evas/strict_current`, `evas/profile_fast_skip_source_error_control`, `spectre/reference_strict_primary`.
- Metrics: behavior PASS, equivalence gate PASS, relative RMS, row-mean relative RMS, max RMS voltage error, max point voltage error, event/digital mismatch.
- Setup details: run EVAS modes once reference CSVs exist; compare EVAS CSVs to the strict reference CSVs.
- Success criterion: fast EVAS has the same PASS count as strict EVAS and no material metric regression.
- Failure interpretation: if fast EVAS regresses only on isolated event-dense rows, keep current speed claim but scope future optimization to those rows.
- Priority: MUST-RUN.

### B3: Precision Ranking Table

- Claim tested: whether EVAS fast is more, equal, or less reference-consistent than Spectre ax-mode.
- Why this exists: this is the only table that can justify "faster and more accurate than ax-mode."
- Dataset: rows where all systems produced comparable CSVs.
- Compared systems:
  - `spectre/ax_normalized` vs `spectre/reference_strict_primary`
  - `evas/strict_current` vs `spectre/reference_strict_primary`
  - `evas/profile_fast_skip_source_error_control` vs `spectre/reference_strict_primary`
- Metrics:
  - primary: acceptance PASS count, worst-signal relative RMS max, row-mean relative RMS max
  - secondary: max RMS V, max point V, event/digital mismatch, behavior checker notes
  - diagnostic: accepted tran steps and wall time
- Success criterion:
  - weak success: EVAS fast is no worse than ax-mode on PASS count and main error metrics.
  - strong success: EVAS fast is closer than ax-mode on the main error metrics while retaining speedup.
- Failure interpretation:
  - if EVAS fast is equivalent but not closer, claim "faster with Spectre-equivalent behavior."
  - if EVAS fast is worse but still within gate, claim "faster within accepted Spectre-equivalence envelope."
  - if EVAS fast fails gate, do not use fast mode as paper default until fixed.
- Priority: MUST-RUN.

### B4: Same-Server Speed Rerun With Reference Metadata

- Claim tested: speed result remains valid with the refined simulator definitions.
- Why this exists: speed and precision tables must refer to the same simulator labels.
- Dataset: same 259-row speed slice; four clean repeats preferred.
- Compared systems: speed lane uses `spectre/ax_speed`, `spectre/classic`, `evas/strict_current`, `evas/profile_fast_skip_source_error_control`; strict reference timing optional because it may be too slow.
- Metrics: geomean speedup, median speedup, min/max row speedup, PASS count, non-PASS rows, machine/command metadata.
- Setup details: reuse existing same-server runner after labels and report wording are updated.
- Success criterion: fast EVAS retains a material speedup over ax-mode and no EVAS PASS / Spectre FAIL mismatch.
- Failure interpretation: if strict reference overhead is large, keep it as precision reference only, not a speed baseline.
- Priority: MUST-RUN for updated paper tables; strict-reference timing is NICE-TO-HAVE.

### B5: Half-Step Sensitivity

- Claim tested: conclusions are robust to a stricter transient step ceiling.
- Why this exists: reviewers may ask whether preserving task `maxstep` hides error.
- Dataset: 30-row representative subset first; full 259 rows only if cheap.
- Compared systems: `spectre/reference_strict_primary` vs `spectre/reference_strict_halfstep`; then fast EVAS vs both references.
- Metrics: same waveform metrics plus wall time blow-up.
- Setup details: halve explicit `maxstep` values; do not invent a global maxstep for rows that omit one unless a separate appendix rule is documented.
- Success criterion: primary conclusions do not flip on the representative subset.
- Failure interpretation: if half-step changes checker outcomes, inspect whether the task itself is overspecified or the reference condition is too intrusive.
- Priority: NICE-TO-HAVE.

## Run Order

| Milestone | Goal | Runs | Decision gate | Cost | Risk |
| --- | --- | --- | --- | --- | --- |
| M0 | Implement and verify settings-normalized Spectre modes | 10-row pilot | All rows PASS and manifest records command/options/final tran/final simulatorOptions | Low | Injection may alter fragile testbenches |
| M1 | Quantify normalized Spectre ax-mode vs strict reference | 259 rows, one repeat | Self-consistency artifact produced with no blocked rows or documented blockers | Medium | Strict reference may be slow |
| M2 | Compare EVAS modes to strict reference | 259 rows, one repeat | EVAS fast and strict have comparable PASS counts | Medium | CSV signal mismatch or checker mismatch |
| M3 | Build precision-ranking table | Aggregate M1/M2 | Decide allowed paper wording | Low | Metrics may be mixed across waveform/non-waveform rows |
| M4 | Rerun speed table with refined labels | Four clean repeats | Fast EVAS remains materially faster than ax-mode | High | Shared-server noise |
| M5 | Half-step sensitivity | 30-row subset | No conclusion flip | Medium | Large runtime increase |

## Must-Run Commands To Add Or Generalize

1. Add runner modes for `spectre/reference_strict_primary`, `spectre/ax_normalized`, and the explicit alias `spectre/ax_speed`.
2. Emit a per-row `simulator_settings_manifest` with:
   - source testbench path
   - final staged testbench path
   - Spectre command
   - injected `simulatorOptions`
   - final `tran` line
   - mode label
3. Generalize `report_spectre_mode_self_consistency.py` so it can compare any two Spectre modes, not only ax-mode/classic.
4. Add an EVAS-vs-strict-reference report path using the existing waveform comparator.
5. Generate one final Markdown table with `spectre/ax_normalized`, `evas/strict_current`, and `evas/fast` all measured against `spectre/reference_strict_primary`.

## Paper Decision Rules

| Observed result | Allowed wording |
| --- | --- |
| EVAS fast faster than ax-speed, all gates PASS, but not closer to strict reference | "EVAS fast is faster while preserving Spectre-equivalent behavior." |
| EVAS fast faster than ax-speed and no worse than ax-normalized vs strict reference | "EVAS fast is faster than the Spectre ax-mode speed baseline and at least as reference-consistent under settings-normalized comparison." |
| EVAS fast faster than ax-speed and clearly closer than ax-normalized vs strict reference | "EVAS fast is faster than the Spectre ax-mode speed baseline and more reference-consistent under settings-normalized comparison." |
| EVAS fast fails strict reference gates | Do not use fast mode as default claim; treat as optimization candidate requiring fixes. |

## Stop Conditions

- Stop after M0 if settings normalization changes too many task outcomes; revise reference rules before running the full slice.
- Stop after M1 if Spectre ax-mode vs strict reference has widespread blocked comparisons due to signal/output mismatch; fix the comparison harness first.
- Stop after M2 if EVAS fast produces any EVAS PASS / strict-reference FAIL that strict EVAS does not produce; diagnose before speed reruns.

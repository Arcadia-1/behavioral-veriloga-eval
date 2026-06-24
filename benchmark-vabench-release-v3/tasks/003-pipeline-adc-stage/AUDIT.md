# Task 003 Audit

Task: `003-pipeline-adc-stage`

Status: certified EVAS formal candidate.

## Four-Standard Review

- Useful scenario: pass. A 1.5-bit pipeline ADC MDAC stage is a common behavioral block for data-converter modeling and mixed-signal verification.
- Reasonable task: pass. The public prompt fixes the module name, positional port order, voltage-domain clocking contract, decision thresholds, output codes, residue formula, clamp behavior, and transition-driven outputs.
- Complete tests: designed for EVAS formal-candidate scope. The visible smoke covers basic compile and the three decision regions. The hidden testbench covers middle, upper, lower, rail-clamp endpoints, and near-threshold cases around `Vcm +/- VREF/4`.
- Fair evaluation: pass for the stated prompt. Hidden checks only score requirements that are stated in `instruction.md`; the public smoke is useful but does not expose the full hidden sequence.

## Checker Contract

The evaluator should save scalar traces named `time`, `phi1`, `phi2`, `vin`, `vres`, `d1`, and `d0`.

The existing `pipeline_stage` checker samples after rising `phi2` edges, classifies `vin` relative to `0.45 +/- 0.9/4`, verifies the expected `(d1,d0)` code, compares `vres` to the clamped gain-two MDAC formula with a 40 mV tolerance, and rejects any residue outside the supply range.

## Evidence

- Static structure: release-v3 files are present with no `meta.json`.
- Static guardrail: `starter/`, `solution/`, and `negative_variants/` do not contain current-domain `I(` contributions, `ddt(`, or `idt(`.
- Hidden gold: PASS under EVAS with `v3_003_pipeline_adc_stage`.
- Concrete negative variants: 5/5 compile and fail with `FAIL_SIM_CORRECTNESS`.

Negative coverage:

- `neg_001_threshold_too_wide`: rejects wrong `VREF/3` sub-ADC thresholds.
- `neg_002_slow_output_edges`: rejects missing upper-region decision and excessive settling time.
- `neg_003_residue_feedback_sign_swapped`: rejects wrong MDAC feedback polarity.
- `neg_004_middle_code_wrong`: rejects wrong middle-region output code.
- `neg_005_residue_gain_low`: rejects wrong residue gain.

## Remaining Risk

- This audit is EVAS-only. Per SOP, paper-facing final certification still needs Spectre/Spectre-AX parity or an explicit EVAS-only label.

Certification status: certified as an EVAS formal candidate on 2026-06-24.

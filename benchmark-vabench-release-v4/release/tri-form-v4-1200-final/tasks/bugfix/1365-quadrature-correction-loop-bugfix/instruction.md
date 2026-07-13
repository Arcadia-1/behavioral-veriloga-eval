# Quadrature Correction Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `quad_corr_top.va`: `quad_corr_top`
- `gain_trim.va`: `gain_trim`
- `skew_estimator.va`: `skew_estimator`
- `corrector.va`: `corrector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_CLEAR`: Reset clears both trim buses, corrected outputs, error metric, and lock state.
- `P_TRIM_DIRECTION`: Enabled calibration updates signed gain and phase trim codes in directions that reduce measured amplitude and quadrature errors.
- `P_CORRECTION_APPLICATION`: Corrected I and Q outputs apply the currently exposed gain and phase trim codes and remain bounded by the supplies.
- `P_LOCK_HOLD`: Lock asserts after three consecutive in-tolerance calibration updates, and disabling calibration holds codes while correction remains active.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `quad_corr_top.va`, `gain_trim.va`, `skew_estimator.va`, `corrector.va`.
Every supplied `.va` file is editable; do not add or omit files.

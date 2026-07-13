# Quadrature Correction Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `quad_corr_top.va`: `quad_corr_top`
- `gain_trim.va`: `gain_trim`
- `skew_estimator.va`: `skew_estimator`
- `corrector.va`: `corrector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_CLEAR`: Reset clears both trim buses, corrected outputs, error metric, and lock state.
- `P_TRIM_DIRECTION`: Enabled calibration updates signed gain and phase trim codes in directions that reduce measured amplitude and quadrature errors.
- `P_CORRECTION_APPLICATION`: Corrected I and Q outputs apply the currently exposed gain and phase trim codes and remain bounded by the supplies.
- `P_LOCK_HOLD`: Lock asserts after three consecutive in-tolerance calibration updates, and disabling calibration holds codes while correction remains active.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `quad_corr_top.va`, `gain_trim.va`, `skew_estimator.va`, `corrector.va`.
Do not add or omit artifacts.

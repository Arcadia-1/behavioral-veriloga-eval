# CDAC Bidirect Residue

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cdac_bidirect_residue.va`: `cdac_bidirect_residue`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SAMPLE_RESIDUE_ON_CLKS_FALL`: At initialization and on each falling `clks` crossing, sample `vin` into the residue state.
- `P_MSB_RESIDUE_STEP_SIGN`: A falling `dctrl7` event adds the half-scale MSB residue step with the declared sign.
- `P_LOWER_BIT_RESIDUE_WEIGHTS`: Falling `dctrl6..dctrl1` events apply the declared binary-weighted residue steps.
- `P_RESIDUE_OUTPUT_GAIN`: `vres` drives the sampled residue with the declared gain and voltage scale.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cdac_bidirect_residue.va`.
Do not add or omit artifacts.

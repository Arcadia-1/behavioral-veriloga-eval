# CDAC 8b Monodown

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cdac_8b_monodown.va`: `cdac_8b_monodown`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_AT_INITIALIZATION_AND_ON_EACH_FALLING`: At initialization and on each falling `clks` crossing, sample `vin` into the held residue. On rising control crossings, subtract the corresponding binary-weighted fraction from the held residue: `dctrl7` subtracts 1/2, `dctrl6` 1/4, continuing down to `dctrl0` at 1/256. Hold the current residue value between events.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cdac_8b_monodown.va`.
Do not add or omit artifacts.

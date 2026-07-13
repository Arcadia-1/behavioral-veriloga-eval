# L2 CDAC 4b Residue

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `l2_cdac_4b_residue.va`: `l2_cdac_4b_residue`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FALLING_CLOCK_SAMPLE`: `vin` is sampled into the residue on initial step and on falling `clks` crossings through `vdd/2`.
- `P_CONTROL_STEP_WEIGHTS`: Rising control crossings add positive capacitive reference steps: `dctrl3` is half scale, `dctrl2` quarter scale, and `dctrl1` eighth scale.
- `P_RETAINED_RESIDUE_OUTPUT`: `vres` retains the accumulated sampled residue between clock/control events.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `l2_cdac_4b_residue.va`.
Do not add or omit artifacts.

# Flash Thermometer Centered Sum

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `flash_thermometer_centered_sum.va`: `flash_thermometer_centered_sum`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_THERMOMETER_THRESHOLD_COUNT`: Each `b0` through `b7` input above `vth` contributes exactly one count to the thermometer total.
- `P_CENTERED_SUM`: The output subtracts the four-count midpoint so the analog sum is centered around zero asserted-input balance.
- `P_OUTPUT_GAIN`: The centered count is multiplied by `gain` and driven on `dout` without extra scaling.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `flash_thermometer_centered_sum.va`.
Do not add or omit artifacts.

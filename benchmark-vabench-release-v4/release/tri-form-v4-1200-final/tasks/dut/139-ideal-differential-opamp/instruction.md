# Ideal Differential Opamp

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `ideal_differential_opamp.va`: `ideal_differential_opamp`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FIXED_COMMON_MODE`: Maintain both outputs symmetric around a fixed 0.5 V common mode.
- `P_DIFFERENTIAL_GAIN_FOUR`: Make the differential output `V(voutp) - V(voutn)` equal to four times `V(vinp, vinn)`.
- `P_OUTPUT_POLARITY`: For positive `V(vinp, vinn)`, drive `voutp` above common mode and `voutn` below common mode.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `ideal_differential_opamp.va`.
Do not add or omit artifacts.

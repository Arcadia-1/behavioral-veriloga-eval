# Hard Voltage Clamp

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `hard_voltage_clamp_behavior.va`: `hard_voltage_clamp_behavior`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_GROUND_REFERENCED_INPUT`: Measure the clamp input as `V(vin, vgnd)` and drive `V(vout, vgnd)` relative to the same reference.
- `P_PASSBAND_TRANSFER`: When the referenced input lies inside `[vclamp_lower, vclamp_upper]`, pass that referenced voltage to the output.
- `P_LOWER_CLAMP`: When the referenced input is below `vclamp_lower`, drive the lower clamp value.
- `P_UPPER_CLAMP`: When the referenced input is above `vclamp_upper`, drive the upper clamp value.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `hard_voltage_clamp_behavior.va`.
Do not add or omit artifacts.

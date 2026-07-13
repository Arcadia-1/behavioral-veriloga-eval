# Soft Voltage Clamp

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `soft_voltage_clamp_behavior.va`: `soft_voltage_clamp_behavior`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_REFERENCED_INPUT_OUTPUT`: Use `V(vin, vgnd)` as input and drive `V(vout, vgnd)` as output.
- `P_LINEAR_MIDDLE_REGION`: Pass the input linearly for `0.0 V <= V(vin, vgnd) <= 0.4 V`.
- `P_SOFT_LOWER_LIMIT`: Below 0.0 V, apply an exponential soft lower limit that approaches -0.2 V with a 0.2 V softness span.
- `P_SOFT_UPPER_LIMIT`: Above 0.4 V, apply an exponential soft upper limit that approaches 0.6 V with a 0.2 V softness span.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `soft_voltage_clamp_behavior.va`.
Do not add or omit artifacts.

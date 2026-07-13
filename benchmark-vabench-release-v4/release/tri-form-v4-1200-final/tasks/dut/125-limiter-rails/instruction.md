# Limiter Rails

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `limiter_rails.va`: `limiter_rails`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RAIL_DERIVED_LIMITS`: Derive the upper limit as `V(vdd) - V(vmax)` and the lower limit as `V(vss) + V(vmin)`.
- `P_PASS_WITHIN_LIMITS`: When `V(vin)` lies between the derived limits, drive `vout` to `V(vin)`.
- `P_LIMIT_ABOVE_UPPER`: When `V(vin)` exceeds the upper limit, drive `vout` to the upper limit.
- `P_LIMIT_BELOW_LOWER`: When `V(vin)` is below the lower limit, drive `vout` to the lower limit.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `limiter_rails.va`.
Do not add or omit artifacts.

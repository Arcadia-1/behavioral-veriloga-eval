# Smooth Absolute Value

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `absolute_value.va`: `absolute_value`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SMOOTH_ABSOLUTE_TRANSFER`: Drive `sigout` as the smooth absolute-value transfer `V(sigin) * tanh(V(sigin) / smooth)`: even in input, nonnegative, deterministic, memoryless, rounded near zero, and asymptotically equal to input magnitude for large positive and negative inputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `absolute_value.va`.
Do not add or omit artifacts.

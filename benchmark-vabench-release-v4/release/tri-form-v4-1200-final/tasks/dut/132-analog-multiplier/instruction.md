# Analog Multiplier

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `analog_multiplier_gain.va`: `analog_multiplier_gain`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ANALOG_PRODUCT`: Drive `sigout` to `V(sigin1) * V(sigin2)` scaled by `gain`, preserving product sign.
- `P_GAIN_PARAMETER_APPLIED`: Apply the overridable `gain` parameter multiplicatively to the input product.
- `P_MULTIPLICATIVE_NOT_ADDITIVE`: The transfer must be multiplicative and must not replace the product with addition or a square of one input.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `analog_multiplier_gain.va`.
Do not add or omit artifacts.

# Safe Voltage Divider

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `safe_voltage_divider.va`: `safe_voltage_divider`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_GAINED_DIVISION`: Drive `sigout` to `gain * V(signumer) / guarded_denominator`.
- `P_DENOMINATOR_MAGNITUDE_FLOOR`: When `abs(V(sigdenom)) < min_sigdenom`, use a denominator magnitude of `min_sigdenom`.
- `P_DENOMINATOR_SIGN_PRESERVED`: Preserve the original denominator sign when applying the minimum denominator guard.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `safe_voltage_divider.va`.
Do not add or omit artifacts.

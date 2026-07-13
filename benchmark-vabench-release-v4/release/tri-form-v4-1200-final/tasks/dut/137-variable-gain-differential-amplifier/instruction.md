# Variable Gain Differential Amplifier

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `variable_gain_differential_amplifier.va`: `variable_gain_differential_amplifier`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DIFFERENTIAL_SIGNAL_AND_CONTROL`: Use `V(sigin_p, sigin_n)` as signal input and `V(sigctrl_p, sigctrl_n)` as gain-control input.
- `P_VARIABLE_GAIN_MIDPOINT`: Drive the unclamped target as `2.0 * V(sigctrl_p, sigctrl_n) * V(sigin_p, sigin_n) + 0.2`.
- `P_OUTPUT_CLAMP`: Clamp the final output target to the inclusive interval `[-0.4 V, 0.8 V]`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `variable_gain_differential_amplifier.va`.
Do not add or omit artifacts.

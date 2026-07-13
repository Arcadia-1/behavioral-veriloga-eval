# Voltage Controlled Gain Amplifier

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `voltage_controlled_gain_amplifier.va`: `voltage_controlled_gain_amplifier`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DIFFERENTIAL_CONTROL`: Use `V(vctrl_p, vctrl_n)` as the gain-control voltage.
- `P_INPUT_OFFSET_AND_GAIN`: Compute the unclamped target as `1.5 * V(vctrl_p, vctrl_n) * (V(vin_p, vin_n) - 0.05) + 0.5`.
- `P_UNIPOLAR_OUTPUT_CLAMP`: Clamp the final output target to the inclusive interval `[0.1 V, 0.9 V]`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `voltage_controlled_gain_amplifier.va`.
Do not add or omit artifacts.

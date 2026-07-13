# Voltage Controlled Gain Amplifier Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `voltage_controlled_gain_amplifier.va`: `voltage_controlled_gain_amplifier`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DIFFERENTIAL_CONTROL`: Use `V(vctrl_p, vctrl_n)` as the gain-control voltage.
- `P_INPUT_OFFSET_AND_GAIN`: Compute the unclamped target as `1.5 * V(vctrl_p, vctrl_n) * (V(vin_p, vin_n) - 0.05) + 0.5`.
- `P_UNIPOLAR_OUTPUT_CLAMP`: Clamp the final output target to the inclusive interval `[0.1 V, 0.9 V]`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `voltage_controlled_gain_amplifier.va`.
Every supplied `.va` file is editable; do not add or omit files.

# Soft Voltage Clamp Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `soft_voltage_clamp_behavior.va`: `soft_voltage_clamp_behavior`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_REFERENCED_INPUT_OUTPUT`: Use `V(vin, vgnd)` as input and drive `V(vout, vgnd)` as output.
- `P_LINEAR_MIDDLE_REGION`: Pass the input linearly for `0.0 V <= V(vin, vgnd) <= 0.4 V`.
- `P_SOFT_LOWER_LIMIT`: Below 0.0 V, apply an exponential soft lower limit that approaches -0.2 V with a 0.2 V softness span.
- `P_SOFT_UPPER_LIMIT`: Above 0.4 V, apply an exponential soft upper limit that approaches 0.6 V with a 0.2 V softness span.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `soft_voltage_clamp_behavior.va`.
Every supplied `.va` file is editable; do not add or omit files.

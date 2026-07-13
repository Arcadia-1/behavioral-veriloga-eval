# Hard Voltage Clamp Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `hard_voltage_clamp_behavior.va`: `hard_voltage_clamp_behavior`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_GROUND_REFERENCED_INPUT`: Measure the clamp input as `V(vin, vgnd)` and drive `V(vout, vgnd)` relative to the same reference.
- `P_PASSBAND_TRANSFER`: When the referenced input lies inside `[vclamp_lower, vclamp_upper]`, pass that referenced voltage to the output.
- `P_LOWER_CLAMP`: When the referenced input is below `vclamp_lower`, drive the lower clamp value.
- `P_UPPER_CLAMP`: When the referenced input is above `vclamp_upper`, drive the upper clamp value.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `hard_voltage_clamp_behavior.va`.
Every supplied `.va` file is editable; do not add or omit files.

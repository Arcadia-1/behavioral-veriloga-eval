# Ideal Differential Opamp Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ideal_differential_opamp.va`: `ideal_differential_opamp`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FIXED_COMMON_MODE`: Maintain both outputs symmetric around a fixed 0.5 V common mode.
- `P_DIFFERENTIAL_GAIN_FOUR`: Make the differential output `V(voutp) - V(voutn)` equal to four times `V(vinp, vinn)`.
- `P_OUTPUT_POLARITY`: For positive `V(vinp, vinn)`, drive `voutp` above common mode and `voutn` below common mode.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ideal_differential_opamp.va`.
Every supplied `.va` file is editable; do not add or omit files.

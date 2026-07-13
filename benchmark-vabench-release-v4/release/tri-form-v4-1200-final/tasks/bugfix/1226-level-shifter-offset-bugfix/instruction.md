# Level Shifter Offset Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `level_shifter_offset.va`: `level_shifter_offset`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DRIVE_SIGOUT_TO_V_SIGIN_PLUS_SIGSHIFT`: Drive `sigout` to `V(sigin) + sigshift` for the current input voltage.
- `P_PRESERVE_UNITY_GAIN_WHILE_ADDING_OFFSET`: Preserve unity gain from `sigin` to `sigout` while adding the configured `sigshift` offset; input changes must appear at `sigout` with the same voltage step size.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `level_shifter_offset.va`.
Every supplied `.va` file is editable; do not add or omit files.

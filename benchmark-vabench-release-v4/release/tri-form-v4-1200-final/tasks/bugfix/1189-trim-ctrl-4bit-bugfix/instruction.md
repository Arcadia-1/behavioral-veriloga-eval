# Trim Ctrl 4bit Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `trim_ctrl_4bit.va`: `trim_ctrl_4bit`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ANALOG_INPUT_ROUNDING`: Round `ain` to the nearest integer code level rather than truncating.
- `P_LOW_FOUR_BIT_MAPPING`: Emit the low four bits of the rounded code on `dout0..dout3` in the declared bit order.
- `P_CONTINUOUS_CODE_UPDATE`: Update deterministically as `ain` changes without requiring hidden state or clocks.
- `P_TRIM_OUTPUT_LEVELS`: All trim outputs are voltage-coded at valid low/high levels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `trim_ctrl_4bit.va`.
Every supplied `.va` file is editable; do not add or omit files.

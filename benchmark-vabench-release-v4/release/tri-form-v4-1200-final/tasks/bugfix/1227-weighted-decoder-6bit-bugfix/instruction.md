# Weighted Decoder 6bit Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `weighted_decoder_6bit.va`: `weighted_decoder_6bit`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_TREAT_EACH_INPUT_AS_LOGIC_1`: Treat each input as logic 1 when its voltage is greater than `vth`, otherwise logic 0.
- `P_INTERPRET_VD1_VD6_AS_AN_UNSIGNED`: Interpret `vd1..vd6` as an unsigned binary word with `vd1` as MSB and `vd6` as LSB.
- `P_SCALE_THE_DECODED_CODE_BY_VREF`: Scale the decoded code by `vref`.
- `P_MAP_ALL_ZERO_INPUT_TO_0`: Map all-zero input to 0 V.
- `P_MAP_ALL_ONES_INPUT_TO_VREF`: Map all-ones input to `vref`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `weighted_decoder_6bit.va`.
Every supplied `.va` file is editable; do not add or omit files.

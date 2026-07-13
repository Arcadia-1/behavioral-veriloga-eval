# Cyclic Decoder 12bit Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cyclic_decoder_12bit.va`: `cyclic_decoder_12bit`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RISING_EDGE_12BIT_DECODE`: Each rising `clks` crossing samples the twelve voltage-coded bits into an unsigned code.
- `P_BIT_WEIGHT_ORDER`: `d0` is the LSB and `d11` is the MSB in the decoded code.
- `P_CENTERED_OUTPUT_SCALE`: The decoded value is normalized to the full 12-bit range, shifted by the half-scale midpoint, and held on `dout`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cyclic_decoder_12bit.va`.
Every supplied `.va` file is editable; do not add or omit files.

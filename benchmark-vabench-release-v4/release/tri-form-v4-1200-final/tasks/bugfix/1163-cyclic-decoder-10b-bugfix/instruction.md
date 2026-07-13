# Cyclic Decoder 10b Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cyclic_decoder_10b.va`: `cyclic_decoder_10b`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_READY_SERIAL_CAPTURE`: After each publication clock, rising `ready` crossings collect up to `nbit` serial decisions MSB first.
- `P_TERNARY_WEIGHTING`: For each collected decision, high `dp` adds the full current binary weight and low `dp` with high `dn` adds half of that weight.
- `P_NORMALIZED_MIDSCALE_OUTPUT`: The decoded value is normalized by the public bit depth and shifted by the required midscale offset before driving `dout`.
- `P_CLOCKED_PUBLICATION_HOLD`: `dout` updates from event-driven ready/publication handling and holds between publication events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cyclic_decoder_10b.va`.
Every supplied `.va` file is editable; do not add or omit files.

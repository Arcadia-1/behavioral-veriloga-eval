# Weighted Decoder 7b5 Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `weighted_decoder_7b5.va`: `weighted_decoder_7b5`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SHARED_272_DENOMINATOR`: All decoded outputs use the shared normalization denominator of 272.0, including the fixed reference basis.
- `P_SEVEN_BIT_OUTPUT`: `aout7b` reports the 7-bit decoded analog output with the specified redundant SAR weights.
- `P_SEVEN_HALF_BIT_OUTPUT`: `aout7b5` preserves the half-bit redundant contribution and correct polarity.
- `P_EIGHT_BIT_OUTPUT`: `aout8b` reports the full 8-bit weighted output with the correct amplitude.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `weighted_decoder_7b5.va`.
Every supplied `.va` file is editable; do not add or omit files.

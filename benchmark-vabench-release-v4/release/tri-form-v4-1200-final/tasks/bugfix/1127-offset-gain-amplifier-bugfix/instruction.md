# Offset Gain Amplifier Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `offset_gain_amplifier.va`: `offset_gain_amplifier`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INPUT_OFFSET_SUBTRACTION`: Subtract 0.2 V from `V(sigin)` before applying gain.
- `P_FIXED_GAIN_THREE`: Drive `sigout` to `3.0 * (V(sigin) - 0.2)`.
- `P_DIRECT_MEMORYLESS_OUTPUT`: Use a direct memoryless voltage output without clipping, filtering, current output, or stimulus-specific behavior.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `offset_gain_amplifier.va`.
Every supplied `.va` file is editable; do not add or omit files.

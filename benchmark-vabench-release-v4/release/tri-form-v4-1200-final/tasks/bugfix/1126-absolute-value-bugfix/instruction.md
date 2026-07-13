# Absolute Value Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `absolute_value_behavior.va`: `absolute_value_behavior`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_POSITIVE_INPUT_PASSTHROUGH`: For nonnegative `V(sigin)`, drive `sigout` to the same nonnegative voltage.
- `P_NEGATIVE_INPUT_REFLECTION`: For negative `V(sigin)`, drive `sigout` to `-V(sigin)`.
- `P_MEMORYLESS_ABSOLUTE_VALUE`: The output is an instantaneous absolute-value function of `sigin` with no retained state or waveform schedule.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `absolute_value_behavior.va`.
Every supplied `.va` file is editable; do not add or omit files.

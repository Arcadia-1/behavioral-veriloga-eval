# Reference Ladder with Buffered Taps Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `reference_ladder_buffered_taps.va`: `reference_ladder_buffered_taps`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive taps to `vss` and clear `monotonic_ok`.
- `P_WHEN_ENABLED_GENERATE_FOUR_EVENLY_SPACED`: When enabled, generate four evenly spaced buffered tap voltages between `vref_lo` and `vref_hi`.
- `P_CLAMP_REVERSED_OR_OUT_OF_RANGE`: Clamp reversed or out-of-range references into the public rail range before generating taps.
- `P_ASSERT_MONOTONIC_OK_ONLY_WHEN_THE`: Assert `monotonic_ok` only when the exposed tap sequence is nondecreasing.
- `P_SMOOTH_TAP_OUTPUT_TRANSITIONS_WITH_THE`: Smooth tap output transitions with the public transition parameter.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `reference_ladder_buffered_taps.va`.
Every supplied `.va` file is editable; do not add or omit files.

# Ideal Clkmux 8channel Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ideal_clkmux_8channel.va`: `ideal_clkmux_8channel`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_MODULO8_COUNTER`: The internal selector starts at zero and increments modulo eight on each rising `clk` crossing through 0.5 V.
- `P_INCREMENT_BEFORE_SELECTION`: The first qualifying clock event selects the incremented counter state rather than the reset state.
- `P_ANALOG_CHANNEL_MUX`: `out` follows the input channel selected by the current counter value.
- `P_COUNTER_MONITOR_LEVEL`: `count_x` reports the current selector count with the specified voltage scaling.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ideal_clkmux_8channel.va`.
Every supplied `.va` file is editable; do not add or omit files.

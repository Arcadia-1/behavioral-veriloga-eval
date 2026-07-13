# Two Period Sample Delay Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `two_period_sample_delay.va`: `two_period_sample_delay`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_TWO_PERIOD_DELAY_STATE`: On each rising `update` crossing through `vth`, `aout` updates to the value sampled on the previous update event, then captures the current `ain` for the next event.
- `P_INITIAL_OUTPUT_VALUE`: Before enough update events have occurred, the retained samples and `aout` start from `init`.
- `P_OUTPUT_GAIN_AND_HOLD`: The held `aout` value matches the delayed sample amplitude without gain scaling between update events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `two_period_sample_delay.va`.
Every supplied `.va` file is editable; do not add or omit files.

# Four Channel Edge Sampler Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `four_channel_edge_sampler.va`: `four_channel_edge_sampler`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CONFIGURED_EDGE_SIMULTANEOUS_SAMPLE`: The configured `clk` crossing direction samples `vin0` through `vin3` simultaneously and updates all held outputs together.
- `P_CHANNEL_MAPPING`: Each sampled input channel maps to the same-numbered output channel without swaps.
- `P_OUTPUT_GAIN_AND_HOLD`: Each `vout` holds the sampled amplitude without gain scaling until the next sampling edge.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `four_channel_edge_sampler.va`.
Every supplied `.va` file is editable; do not add or omit files.

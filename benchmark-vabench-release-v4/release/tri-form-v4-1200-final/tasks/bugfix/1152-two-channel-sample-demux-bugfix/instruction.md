# Two Channel Sample Demux Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `two_channel_sample_demux.va`: `two_channel_sample_demux`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCKED_CHANNEL_SELECTION`: A rising `clks1` crossing samples `samp1` and a rising `clks2` crossing samples `samp2` into the shared held output.
- `P_BOTH_CHANNELS_REACHABLE`: Both clocked sample channels can independently update `vout` without one channel masking the other.
- `P_OUTPUT_GAIN_AND_HOLD`: `vout` holds the selected sample amplitude without gain scaling between clock events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `two_channel_sample_demux.va`.
Every supplied `.va` file is editable; do not add or omit files.

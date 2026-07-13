# Resettable DAC Restore 7bit Clocked Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dac_restore_7bit_clocked.va`: `dac_restore_7bit_clocked`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_WHEN_RST_RISES_ABOVE_THRESHOLD_IMMEDIATELY`: When `rst` rises above threshold, immediately restore `vout` to the midscale value of 0 V. While `rst` remains high, ignore clock edges and hold the restored midscale value. When `rst` is low, each rising `clk` crossing decodes `d6..d0` as a 7-bit binary word and drives `vout` to the center of that code bin across a bipolar 1.8 V span from `-0.9 V` to `+0.9 V`. Hold the output between clock events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dac_restore_7bit_clocked.va`.
Every supplied `.va` file is editable; do not add or omit files.

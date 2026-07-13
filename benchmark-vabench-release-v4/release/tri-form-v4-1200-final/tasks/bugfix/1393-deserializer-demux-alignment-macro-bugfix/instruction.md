# Deserializer DEMUX Alignment Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `deserializer_demux_alignment_macro.va`: `deserializer_demux_alignment_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear all parallel outputs, `phase_metric`, and `word_valid`.
- `P_A_RISING_ALIGN_PULSE_RESETS_THE`: A rising `align_pulse` resets the slot pointer so the next sampled serial bit is written to `out0`.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, sample `serial_in` into the active output slot and advance the slot pointer.
- `P_ASSERT_WORD_VALID_AFTER_ALL_FOUR`: Assert `word_valid` after all four output slots have been updated since the most recent alignment event.
- `P_PHASE_METRIC_MUST_EXPOSE_THE_ACTIVE`: `phase_metric` must expose the active slot pointer.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `deserializer_demux_alignment_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.

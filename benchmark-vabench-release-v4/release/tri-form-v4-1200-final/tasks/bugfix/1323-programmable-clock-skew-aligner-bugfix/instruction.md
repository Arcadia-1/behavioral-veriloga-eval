# Programmable Clock Skew Aligner Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `programmable_clock_skew_aligner.va`: `programmable_clock_skew_aligner`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive output and metrics low.
- `P_DECODE_SKEW_2_SKEW_0_AS`: Decode `skew_2..skew_0` as a programmable output-edge delay code.
- `P_FOR_EACH_ACCEPTED_INPUT_CLOCK_EDGE`: For each accepted input clock edge, schedule one output edge after the code-dependent delay.
- `P_EXPOSE_THE_ACTIVE_DELAY_CODE_AS`: Expose the active delay code as `delay_metric`.
- `P_ASSERT_VALID_AFTER_THE_FIRST_DELAYED`: Assert `valid` after the first delayed output edge has been generated.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `programmable_clock_skew_aligner.va`.
Every supplied `.va` file is editable; do not add or omit files.

# Serializer MUX Timing Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `serializer_mux_timing_macro.va`: `serializer_mux_timing_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear `serial_out`, slot outputs, and `valid`.
- `P_WHEN_ENABLED_STEP_THROUGH_INPUTS_D0`: When enabled, step through inputs `d0`, `d1`, `d2`, and `d3` on successive rising `clk` edges.
- `P_DRIVE_SERIAL_OUT_AS_THE_VOLTAGE`: Drive `serial_out` as the voltage-coded value of the active input slot.
- `P_SLOT_1_SLOT_0_MUST_EXPOSE`: `slot_1..slot_0` must expose the active slot index.
- `P_ASSERT_VALID_AFTER_THE_FIRST_COMPLETE`: Assert `valid` after the first complete four-slot frame.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `serializer_mux_timing_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.

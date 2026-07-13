# Instrumentation Amplifier Offset-trim System Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `instrumentation_amp_offset_trim_top.va`: `instrumentation_amp_offset_trim_top`
- `diff_gain_core.va`: `diff_gain_core`
- `offset_trim_controller.va`: `offset_trim_controller`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_CLEAR_THE_TRIM_STATE`: On reset, clear the trim state, drive `vout` to `vcm`, clear `offset_metric`, and clear `ready`.
- `P_DECODE_TRIM_2_TRIM_0_AS`: Decode `trim_2..trim_0` as a signed offset correction around zero.
- `P_WHILE_CAL_EN_IS_HIGH_UPDATE`: While `cal_en` is high, update the internal trim accumulator once per rising `clk` edge toward reducing the measured input offset.
- `P_DRIVE_VOUT_FROM_THE_CORRECTED_DIFFERENTIAL`: Drive `vout` from the corrected differential input and clamp to the output rails.
- `P_EXPOSE_THE_ACTIVE_CORRECTION_ON_OFFSET`: Expose the active correction on `offset_metric` and assert `ready` after three calibration updates.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `instrumentation_amp_offset_trim_top.va`, `diff_gain_core.va`, `offset_trim_controller.va`.
Every supplied `.va` file is editable; do not add or omit files.

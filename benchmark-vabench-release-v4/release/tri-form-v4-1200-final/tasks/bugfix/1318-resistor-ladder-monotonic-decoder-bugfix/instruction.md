# Resistor Ladder Monotonic Decoder Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `resistor_ladder_monotonic_decoder.va`: `resistor_ladder_monotonic_decoder`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` low, clear `step_metric`, and clear `monotonic_ok`.
- `P_DECODE_CODE_2_CODE_0_AS`: Decode `code_2..code_0` as an unsigned ladder tap index from 0 to 7.
- `P_DRIVE_VOUT_TO_THE_CORRESPONDING_EVENLY`: Drive `vout` to the corresponding evenly spaced ladder voltage between `vss` and `vdd`.
- `P_EXPOSE_ONE_LSB_STEP_ON_STEP`: Expose one LSB step on `step_metric` while enabled.
- `P_ASSERT_MONOTONIC_OK_WHEN_THE_ACTIVE`: Assert `monotonic_ok` when the active code-to-output mapping is nondecreasing.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `resistor_ladder_monotonic_decoder.va`.
Every supplied `.va` file is editable; do not add or omit files.

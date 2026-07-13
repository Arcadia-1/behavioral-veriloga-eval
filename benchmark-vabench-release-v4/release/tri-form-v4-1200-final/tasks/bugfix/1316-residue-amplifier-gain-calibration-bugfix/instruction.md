# Residue Amplifier Gain-calibration Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `residue_amp_gain_calibration_top.va`: `residue_amp_gain_calibration_top`
- `residue_amp_core.va`: `residue_amp_core`
- `gain_cal_controller.va`: `gain_cal_controller`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_CLEAR_GAIN_CODE_OUTPUT`: On reset, clear gain code, output, error metric, and `locked`.
- `P_WHILE_CAL_EN_IS_HIGH_COMPARE`: While `cal_en` is high, compare the current residue output against `residue_ref` on each rising `clk` edge.
- `P_INCREMENT_OR_DECREMENT_THE_GAIN_CODE`: Increment or decrement the gain code by one step to reduce the signed error.
- `P_DRIVE_VOUT_AS_A_CLAMPED_RESIDUE`: Drive `vout` as a clamped residue-amplified version of `vin - vcm` using the active gain code.
- `P_ASSERT_LOCKED_AFTER_THREE_CONSECUTIVE_UPDATES`: Assert `locked` after three consecutive updates with error magnitude below `lock_tol`.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `residue_amp_gain_calibration_top.va`, `residue_amp_core.va`, `gain_cal_controller.va`.
Every supplied `.va` file is editable; do not add or omit files.

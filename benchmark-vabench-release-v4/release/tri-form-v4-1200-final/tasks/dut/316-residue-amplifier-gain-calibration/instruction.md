# Residue Amplifier Gain-calibration Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `residue_amp_gain_calibration_top.va`: `residue_amp_gain_calibration_top`
- `residue_amp_core.va`: `residue_amp_core`
- `gain_cal_controller.va`: `gain_cal_controller`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_CLEAR_GAIN_CODE_OUTPUT`: On reset, clear gain code, output, error metric, and `locked`.
- `P_WHILE_CAL_EN_IS_HIGH_COMPARE`: While `cal_en` is high, compare the current residue output against `residue_ref` on each rising `clk` edge.
- `P_INCREMENT_OR_DECREMENT_THE_GAIN_CODE`: Increment or decrement the gain code by one step to reduce the signed error.
- `P_DRIVE_VOUT_AS_A_CLAMPED_RESIDUE`: Drive `vout` as a clamped residue-amplified version of `vin - vcm` using the active gain code.
- `P_ASSERT_LOCKED_AFTER_THREE_CONSECUTIVE_UPDATES`: Assert `locked` after three consecutive updates with error magnitude below `lock_tol`.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `residue_amp_gain_calibration_top.va`, `residue_amp_core.va`, `gain_cal_controller.va`.
Do not add or omit artifacts.

# Instrumentation Amplifier Offset-trim System

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `instrumentation_amp_offset_trim_top.va`: `instrumentation_amp_offset_trim_top`
- `diff_gain_core.va`: `diff_gain_core`
- `offset_trim_controller.va`: `offset_trim_controller`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_CLEAR_THE_TRIM_STATE`: On reset, clear the trim state, drive `vout` to `vcm`, clear `offset_metric`, and clear `ready`.
- `P_DECODE_TRIM_2_TRIM_0_AS`: Decode `trim_2..trim_0` as a signed offset correction around zero.
- `P_WHILE_CAL_EN_IS_HIGH_UPDATE`: While `cal_en` is high, update the internal trim accumulator once per rising `clk` edge toward reducing the measured input offset.
- `P_DRIVE_VOUT_FROM_THE_CORRECTED_DIFFERENTIAL`: Drive `vout` from the corrected differential input and clamp to the output rails.
- `P_EXPOSE_THE_ACTIVE_CORRECTION_ON_OFFSET`: Expose the active correction on `offset_metric` and assert `ready` after three calibration updates.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `instrumentation_amp_offset_trim_top.va`, `diff_gain_core.va`, `offset_trim_controller.va`.
Do not add or omit artifacts.

# Capacitor Mismatch Calibration Engine

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `capacitor_mismatch_cal_engine_top.va`: `capacitor_mismatch_cal_engine_top`
- `cal_code_accumulator.va`: `cal_code_accumulator`
- `correction_metric_dac.va`: `correction_metric_dac`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear the calibration code, metric, and `done`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, update a signed correction accumulator using the sign of `err_in - vcm`.
- `P_SATURATE_THE_PUBLIC_4_BIT_CALIBRATION`: Saturate the public 4-bit calibration code at the endpoints.
- `P_DRIVE_CORRECTION_METRIC_AS_THE_VOLTAGE`: Drive `correction_metric` as the voltage-coded correction applied by the active code.
- `P_ASSERT_DONE_AFTER_EIGHT_ENABLED_UPDATES`: Assert `done` after eight enabled updates or when the error remains within `err_tol` for two updates.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `capacitor_mismatch_cal_engine_top.va`, `cal_code_accumulator.va`, `correction_metric_dac.va`.
Do not add or omit artifacts.

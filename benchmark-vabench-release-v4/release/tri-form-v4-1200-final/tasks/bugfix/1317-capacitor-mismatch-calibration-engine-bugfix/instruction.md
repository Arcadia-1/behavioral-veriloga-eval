# Capacitor Mismatch Calibration Engine Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `capacitor_mismatch_cal_engine_top.va`: `capacitor_mismatch_cal_engine_top`
- `cal_code_accumulator.va`: `cal_code_accumulator`
- `correction_metric_dac.va`: `correction_metric_dac`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear the calibration code, metric, and `done`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, update a signed correction accumulator using the sign of `err_in - vcm`.
- `P_SATURATE_THE_PUBLIC_4_BIT_CALIBRATION`: Saturate the public 4-bit calibration code at the endpoints.
- `P_DRIVE_CORRECTION_METRIC_AS_THE_VOLTAGE`: Drive `correction_metric` as the voltage-coded correction applied by the active code.
- `P_ASSERT_DONE_AFTER_EIGHT_ENABLED_UPDATES`: Assert `done` after eight enabled updates or when the error remains within `err_tol` for two updates.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `capacitor_mismatch_cal_engine_top.va`, `cal_code_accumulator.va`, `correction_metric_dac.va`.
Every supplied `.va` file is editable; do not add or omit files.

# Serializer MUX Timing Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `serializer_mux_timing_macro.va`: `serializer_mux_timing_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear `serial_out`, slot outputs, and `valid`.
- `P_WHEN_ENABLED_STEP_THROUGH_INPUTS_D0`: When enabled, step through inputs `d0`, `d1`, `d2`, and `d3` on successive rising `clk` edges.
- `P_DRIVE_SERIAL_OUT_AS_THE_VOLTAGE`: Drive `serial_out` as the voltage-coded value of the active input slot.
- `P_SLOT_1_SLOT_0_MUST_EXPOSE`: `slot_1..slot_0` must expose the active slot index.
- `P_ASSERT_VALID_AFTER_THE_FIRST_COMPLETE`: Assert `valid` after the first complete four-slot frame.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `serializer_mux_timing_macro.va`.
Do not add or omit artifacts.

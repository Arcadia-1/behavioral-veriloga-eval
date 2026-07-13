# VGA Gain Calibration Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `vga_cal_loop_top.va`: `vga_cal_loop_top`
- `peak_detector.va`: `peak_detector`
- `gain_controller.va`: `gain_controller`
- `vga_model.va`: `vga_model`
- `lock_detector.va`: `lock_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_VGA_RESET_STATE`: Reset restores gain code four and clears peak_metric and locked.
- `P_VGA_PEAK_SAMPLE`: Each enabled rising clock samples the absolute vin magnitude into peak_metric.
- `P_VGA_GAIN_DIRECTION`: The gain code moves one bounded step toward target according to the prior sampled peak and clamps to zero through fifteen.
- `P_VGA_OUTPUT_GAIN`: vout continuously equals vin times gain_min plus gain_lsb times gain code.
- `P_VGA_LOCK_QUALIFICATION`: locked asserts after three consecutive enabled updates whose prior sampled peak lies within tolerance.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `vga_cal_loop_top.va`, `peak_detector.va`, `gain_controller.va`, `vga_model.va`, `lock_detector.va`.
Do not add or omit artifacts.

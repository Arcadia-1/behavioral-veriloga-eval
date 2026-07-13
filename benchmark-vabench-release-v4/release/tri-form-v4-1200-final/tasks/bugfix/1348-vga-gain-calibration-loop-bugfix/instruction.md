# VGA Gain Calibration Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `vga_cal_loop_top.va`: `vga_cal_loop_top`
- `peak_detector.va`: `peak_detector`
- `gain_controller.va`: `gain_controller`
- `vga_model.va`: `vga_model`
- `lock_detector.va`: `lock_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_VGA_RESET_STATE`: Reset restores gain code four and clears peak_metric and locked.
- `P_VGA_PEAK_SAMPLE`: Each enabled rising clock samples the absolute vin magnitude into peak_metric.
- `P_VGA_GAIN_DIRECTION`: The gain code moves one bounded step toward target according to the prior sampled peak and clamps to zero through fifteen.
- `P_VGA_OUTPUT_GAIN`: vout continuously equals vin times gain_min plus gain_lsb times gain code.
- `P_VGA_LOCK_QUALIFICATION`: locked asserts after three consecutive enabled updates whose prior sampled peak lies within tolerance.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `vga_cal_loop_top.va`, `peak_detector.va`, `gain_controller.va`, `vga_model.va`, `lock_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.

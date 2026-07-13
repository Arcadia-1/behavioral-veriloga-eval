# Complete Calibration Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `complete_calibration_loop.va`: `complete_calibration_loop`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_TO_TARGET`: Active-high reset initializes out, trim_mon, residual_mon, and metric to their target-state values.
- `P_CLOCKED_LOOP_UPDATE`: After reset releases, calibration state updates on rising clk crossings and holds between updates.
- `P_RESIDUAL_OBSERVATION`: Residual_mon exposes clamp(target + raw_error + (trim_mon_next - target), vmin, vmax), where raw_error is V(vin)-target and trim_mon_next is the current edge's bounded negative-feedback trim update.
- `P_NEGATIVE_FEEDBACK_DIRECTION`: The trim correction uses trim_mon_next = clamp(trim_mon - loop_gain * residual_before_update, vmin, vmax), so positive residual decreases trim and negative residual increases trim.
- `P_PLANT_CONVERGENCE`: Out follows out_next = clamp(out + plant_alpha * (residual_mon_next - out), vmin, vmax) on each non-reset update.
- `P_BOUNDS_AND_METRIC`: Bounded analog states remain within vmin through vmax, while metric equals clamp(0.9 - 1.5 * abs(out-target), 0.0, 0.9) after each update.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `complete_calibration_loop.va`.
Every supplied `.va` file is editable; do not add or omit files.

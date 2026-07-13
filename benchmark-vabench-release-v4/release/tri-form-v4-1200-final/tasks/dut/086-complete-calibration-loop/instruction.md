# Complete Calibration Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `complete_calibration_loop.va`: `complete_calibration_loop`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_TO_TARGET`: Active-high reset initializes out, trim_mon, residual_mon, and metric to their target-state values.
- `P_CLOCKED_LOOP_UPDATE`: After reset releases, calibration state updates on rising clk crossings and holds between updates.
- `P_RESIDUAL_OBSERVATION`: Residual_mon exposes clamp(target + raw_error + (trim_mon_next - target), vmin, vmax), where raw_error is V(vin)-target and trim_mon_next is the current edge's bounded negative-feedback trim update.
- `P_NEGATIVE_FEEDBACK_DIRECTION`: The trim correction uses trim_mon_next = clamp(trim_mon - loop_gain * residual_before_update, vmin, vmax), so positive residual decreases trim and negative residual increases trim.
- `P_PLANT_CONVERGENCE`: Out follows out_next = clamp(out + plant_alpha * (residual_mon_next - out), vmin, vmax) on each non-reset update.
- `P_BOUNDS_AND_METRIC`: Bounded analog states remain within vmin through vmax, while metric equals clamp(0.9 - 1.5 * abs(out-target), 0.0, 0.9) after each update.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `complete_calibration_loop.va`.
Do not add or omit artifacts.

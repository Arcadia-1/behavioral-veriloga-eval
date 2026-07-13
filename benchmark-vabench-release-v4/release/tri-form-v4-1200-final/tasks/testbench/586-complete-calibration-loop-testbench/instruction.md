# Complete Calibration Loop Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Complete Calibration Loop` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_RESET_TO_TARGET`: Active-high reset initializes out, trim_mon, residual_mon, and metric to their target-state values.
- `P_CLOCKED_LOOP_UPDATE`: After reset releases, calibration state updates on rising clk crossings and holds between updates.
- `P_RESIDUAL_OBSERVATION`: Residual_mon exposes clamp(target + raw_error + (trim_mon_next - target), vmin, vmax), where raw_error is V(vin)-target and trim_mon_next is the current edge's bounded negative-feedback trim update.
- `P_NEGATIVE_FEEDBACK_DIRECTION`: The trim correction uses trim_mon_next = clamp(trim_mon - loop_gain * residual_before_update, vmin, vmax), so positive residual decreases trim and negative residual increases trim.
- `P_PLANT_CONVERGENCE`: Out follows out_next = clamp(out + plant_alpha * (residual_mon_next - out), vmin, vmax) on each non-reset update.
- `P_BOUNDS_AND_METRIC`: Bounded analog states remain within vmin through vmax, while metric equals clamp(0.9 - 1.5 * abs(out-target), 0.0, 0.9) after each update.

The required trace names are: `time`, `clk`, `rst`, `vin`, `out`, `metric`, `trim_mon`, `residual_mon`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.

# VGA Gain Calibration Loop Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `VGA Gain Calibration Loop` DUT. The evaluator runs the same submitted bytes
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

- `P_VGA_RESET_STATE`: Reset restores gain code four and clears peak_metric and locked.
- `P_VGA_PEAK_SAMPLE`: Each enabled rising clock samples the absolute vin magnitude into peak_metric.
- `P_VGA_GAIN_DIRECTION`: The gain code moves one bounded step toward target according to the prior sampled peak and clamps to zero through fifteen.
- `P_VGA_OUTPUT_GAIN`: vout continuously equals vin times gain_min plus gain_lsb times gain code.
- `P_VGA_LOCK_QUALIFICATION`: locked asserts after three consecutive enabled updates whose prior sampled peak lies within tolerance.

The required trace names are: `time`, `vin`, `target`, `clk`, `rst`, `start`, `vout`, `gain_3`, `gain_2`, `gain_1`, `gain_0`, `locked`, `peak_metric`.

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

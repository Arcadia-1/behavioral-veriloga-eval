# Baseband AGC and Filter Chain Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Baseband AGC and Filter Chain` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation restores gain code 4, clears metrics and flags, and drives vout to vcm.
- `P_LEVEL_GAIN_CONTROL`: Each enabled rising clock samples the input magnitude and moves the bounded gain code toward the target deadband.
- `P_VGA_FILTER_RESPONSE`: The VGA applies gain_min plus gain_lsb times code and the sampled filter moves by alpha toward that VGA result.
- `P_CLIP_AND_SETTLE`: clip_flag reports an unclamped filter excursion beyond the rails and settled asserts only after three consecutive in-tolerance updates.

The required trace names are: `time`, `vin`, `target`, `clk`, `rst`, `enable`, `vout`, `gain_3`, `gain_2`, `gain_1`, `gain_0`, `level_metric`, `clip_flag`, `settled`.

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

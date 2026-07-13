# Residue Amplifier Gain-calibration Loop Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Residue Amplifier Gain-calibration Loop` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_CLEAR_GAIN_CODE_OUTPUT`: On reset, clear gain code, output, error metric, and `locked`.
- `P_WHILE_CAL_EN_IS_HIGH_COMPARE`: While `cal_en` is high, compare the current residue output against `residue_ref` on each rising `clk` edge.
- `P_INCREMENT_OR_DECREMENT_THE_GAIN_CODE`: Increment or decrement the gain code by one step to reduce the signed error.
- `P_DRIVE_VOUT_AS_A_CLAMPED_RESIDUE`: Drive `vout` as a clamped residue-amplified version of `vin - vcm` using the active gain code.
- `P_ASSERT_LOCKED_AFTER_THREE_CONSECUTIVE_UPDATES`: Assert `locked` after three consecutive updates with error magnitude below `lock_tol`.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vin`, `residue_ref`, `clk`, `rst`, `cal_en`, `gain_2`, `gain_1`, `gain_0`, `vout`, `error_metric`, `locked`.

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

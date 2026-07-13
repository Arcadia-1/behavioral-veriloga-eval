# Instrumentation Amplifier Offset-trim System Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Instrumentation Amplifier Offset-trim System` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_CLEAR_THE_TRIM_STATE`: On reset, public outputs are held clear; trim controller state is cleared on a rising `clk` sampled while `rst` is high, driving `vout` to `vcm`, clearing `offset_metric`, and clearing `ready`. This must be observable both at initial reset and at a later reset after nonzero calibration state has developed.
- `P_DECODE_TRIM_2_TRIM_0_AS`: Decode `trim_2..trim_0` as an unsigned code with weights 4/2/1, map `signed_code = code - 4`, and form the static correction `signed_code * trim_lsb`; the testbench should exercise trim codes on both sides of zero rather than a single static trim value.
- `P_WHILE_CAL_EN_IS_HIGH_UPDATE`: While `cal_en` is high, update the adaptive trim once per rising `clk`: compare `vinp-vinn` against the static plus adaptive correction, increment by `trim_lsb` above `+0.5*trim_lsb`, decrement below `-0.5*trim_lsb`, and hold state when `cal_en` is low.
- `P_DRIVE_VOUT_FROM_THE_CORRECTED_DIFFERENTIAL`: Drive `vout` from the corrected differential input `vcm + diff_gain*(vinp-vinn-(corr-vcm))` clamped to the rails; include positive and negative input differential cases so output gain polarity and correction polarity are observable.
- `P_EXPOSE_THE_ACTIVE_CORRECTION_ON_OFFSET`: `offset_metric` exposes the active correction voltage and `ready` asserts only after at least three enabled calibration updates, while remaining deasserted before those updates and after reset clears state.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vinp`, `vinn`, `clk`, `rst`, `cal_en`, `trim_2`, `trim_1`, `trim_0`, `vout`, `offset_metric`, `ready`.

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

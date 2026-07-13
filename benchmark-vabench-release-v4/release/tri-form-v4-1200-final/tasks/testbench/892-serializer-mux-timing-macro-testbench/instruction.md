# Serializer MUX Timing Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Serializer MUX Timing Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear `serial_out`, slot outputs, and `valid`.
- `P_WHEN_ENABLED_STEP_THROUGH_INPUTS_D0`: When enabled, step through inputs `d0`, `d1`, `d2`, and `d3` on successive rising `clk` edges.
- `P_DRIVE_SERIAL_OUT_AS_THE_VOLTAGE`: Drive `serial_out` as the voltage-coded value of the active input slot.
- `P_SLOT_1_SLOT_0_MUST_EXPOSE`: `slot_1..slot_0` must expose the active slot index.
- `P_ASSERT_VALID_AFTER_THE_FIRST_COMPLETE`: Assert `valid` after the first complete four-slot frame.

The required trace names are: `time`, `clk`, `rst`, `enable`, `d0`, `d1`, `d2`, `d3`, `serial_out`, `slot_1`, `slot_0`, `valid`.

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

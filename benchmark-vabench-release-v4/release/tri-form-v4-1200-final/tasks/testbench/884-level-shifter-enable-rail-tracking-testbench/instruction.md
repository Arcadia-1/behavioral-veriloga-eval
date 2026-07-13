# Level Shifter with Enable and Rail Tracking Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Level Shifter with Enable and Rail Tracking` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_OR_LOW_ENABLE_DRIVES_VOUT`: Reset or low `enable` drives `vout` to `vss` and clears `valid`.
- `P_WHEN_ENABLED_COMPARE_VIN_AGAINST_HALF`: When enabled, compare `vin` against half of the sensed low-side rail `vddl`.
- `P_DRIVE_VOUT_TO_VDDH_FOR_A`: Drive `vout` to `vddh` for a high input and to `vss` for a low input.
- `P_VALID_IS_HIGH_ONLY_WHEN_ENABLED`: `valid` is high only when enabled, not reset, and the high-side rail is above the minimum valid rail.
- `P_THE_OUTPUT_HIGH_LEVEL_MUST_TRACK`: The output high level must track changes in `vddh`; it must not use a fixed internal high level.

The required trace names are: `time`, `vin`, `enable`, `rst`, `vddl`, `vddh`, `vout`, `valid`.

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

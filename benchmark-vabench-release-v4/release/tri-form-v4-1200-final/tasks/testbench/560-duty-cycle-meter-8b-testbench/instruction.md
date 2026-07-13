# Duty Cycle Meter 8b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Duty Cycle Meter 8b` DUT. The evaluator runs the same submitted bytes
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

- `P_COMPLETE_CYCLE_MEASUREMENT`: A new duty result is produced only after observing a rising edge, one intervening falling edge, and the next rising edge.
- `P_HIGH_FRACTION_CODE`: For each complete cycle, the unsigned code is the rounded value of 255 times high time divided by period.
- `P_CODE_SATURATION`: The reported duty code is saturated to the inclusive range 0 through 255.
- `P_VALID_HOLD`: valid remains low before the first complete measurement and asserts and holds high after a duty result is available.
- `P_BIT_ORDER_AND_LEVELS`: duty0 is the least significant bit and duty7 is the most significant bit; asserted outputs use vdd and inactive outputs use 0 V.

The required trace names are: `time`, `clk_in`, `valid`, `duty0`, `duty1`, `duty2`, `duty3`, `duty4`, `duty5`, `duty6`, `duty7`.

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

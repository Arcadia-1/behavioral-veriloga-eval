# Event Counter Windowed 16b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Event Counter Windowed 16b` DUT. The evaluator runs the same submitted bytes
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

- `P_WINDOW_OPEN`: A rising gate crossing clears the count, opens a new measurement window, and drives done low.
- `P_IN_WINDOW_COUNT`: Each rising event crossing increments the count exactly once only while the window is active and gate is high.
- `P_OUT_OF_WINDOW_IGNORE`: Event crossings before a window opens or after it closes do not change the held result.
- `P_WINDOW_CLOSE_HOLD`: A falling gate crossing closes the window, preserves the final count, and asserts done.
- `P_BIT_ORDER_AND_LEVELS`: count0 is the least significant bit and count15 is the most significant bit; asserted outputs use vdd and inactive outputs use 0 V.

The required trace names are: `time`, `gate`, `event`, `done`, `count0`, `count1`, `count2`, `count3`, `count4`, `count5`, `count6`, `count7`, `count8`, `count9`, `count10`, `count11`, `count12`, `count13`, `count14`, `count15`.

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

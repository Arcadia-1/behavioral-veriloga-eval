# Ideal Clkmux 8channel Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Ideal Clkmux 8channel` DUT. The evaluator runs the same submitted bytes
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

- `P_MODULO8_COUNTER`: The internal selector starts at zero and increments modulo eight on each rising `clk` crossing through 0.5 V.
- `P_INCREMENT_BEFORE_SELECTION`: The first qualifying clock event selects the incremented counter state rather than the reset state.
- `P_ANALOG_CHANNEL_MUX`: `out` follows the input channel selected by the current counter value.
- `P_COUNTER_MONITOR_LEVEL`: `count_x` reports the current selector count with the specified voltage scaling.

The required trace names are: `time`, `clk`, `out`, `count_x`, `in0`, `in1`, `in2`, `in3`, `in4`, `in5`, `in6`, `in7`.

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

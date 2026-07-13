# Multiphase Clock Generator 4ph Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Multiphase Clock Generator 4ph` DUT. The evaluator runs the same submitted bytes
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

- `P_PERIOD`: Each output repeats with a 20 ns period.
- `P_DUTY_CYCLE`: Each output has approximately 50 percent duty cycle.
- `P_PHASE_OFFSETS`: Relative to clk0, corresponding rising edges of clk90, clk180, and clk270 lag by 5 ns, 10 ns, and 15 ns respectively.
- `P_PHASE_STABILITY`: The output phase ordering and offsets remain stable across repeated periods.
- `P_OUTPUT_LEVELS`: All clocks use 0 V and vdd levels with finite transition smoothing set by tr.

The required trace names are: `time`, `clk0`, `clk90`, `clk180`, `clk270`.

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

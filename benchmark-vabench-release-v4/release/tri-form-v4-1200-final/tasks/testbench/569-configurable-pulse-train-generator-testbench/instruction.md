# Configurable Pulse Train Generator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Configurable Pulse Train Generator` DUT. The evaluator runs the same submitted bytes
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

- `P_IDLE_CAPTURE`: A sampled high start while idle captures unsigned period3:period0, width3:width0, and count3:count0 on a rising clk crossing.
- `P_ZERO_CODE_MINIMUM`: A zero-coded period, width, or count is interpreted as one clock sample rather than zero.
- `P_PULSE_COUNT`: Each accepted command emits exactly the captured count number of pulses.
- `P_WIDTH_AND_PERIOD`: Each pulse remains high for the captured width in clock samples and pulse starts are separated by the captured period in clock samples.
- `P_COMPLETION`: After the final pulse completes, pulse is low and done is asserted.
- `P_OUTPUT_LEVELS`: pulse and done use 0 V and vdd levels with finite transition smoothing set by tr.

The required trace names are: `time`, `clk`, `start`, `period0`, `period1`, `period2`, `period3`, `width0`, `width1`, `width2`, `width3`, `count0`, `count1`, `count2`, `count3`, `pulse`, `done`.

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

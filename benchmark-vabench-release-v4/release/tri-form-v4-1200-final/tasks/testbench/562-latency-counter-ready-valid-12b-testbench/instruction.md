# Ready/Valid Latency Counter 12b Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Ready/Valid Latency Counter 12b` DUT. The evaluator runs the same submitted bytes
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

- `P_REQUEST_START`: While idle, a rising clock crossing that samples valid_i high starts a measurement at count zero and clears done.
- `P_WAIT_CYCLE_COUNT`: While active, each rising clock crossing that samples ready_i low increments the pending latency by one cycle.
- `P_READY_COMPLETION`: While active, a rising clock crossing that samples ready_i high latches the current count to lat[11:0], asserts done, and returns the meter to idle.
- `P_ZERO_LATENCY`: If valid_i and ready_i are both high on the starting clock edge, the reported latency is zero.
- `P_RESULT_HOLD_AND_ORDER`: The completed result holds until a later request starts; lat0 is LSB, lat11 is MSB, and asserted outputs use vdd.

The required trace names are: `time`, `clk`, `valid_i`, `ready_i`, `done`, `lat0`, `lat1`, `lat2`, `lat3`, `lat4`, `lat5`, `lat6`, `lat7`, `lat8`, `lat9`, `lat10`, `lat11`.

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

# Flash Data Align Pipeline Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Flash Data Align Pipeline` DUT. The evaluator runs the same submitted bytes
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

- `P_THERMOMETER_COUNT`: At each rising `clk` crossing through `vth`, count all asserted thermometer inputs `din0` through `din7`.
- `P_FOUR_STAGE_ALIGNMENT`: The sampled count is shifted through a four-stage alignment pipeline before it is published.
- `P_BINARY_OUTPUT_ORDER`: The delayed count is driven as voltage-coded binary with `dout0` as LSB and `dout3` as MSB.
- `P_EVENT_HELD_OUTPUTS`: Outputs update only from pipeline clock events and hold their previous voltage-coded state between events.

The required trace names are: `time`, `clk`, `din0`, `din1`, `din2`, `din3`, `din4`, `din5`, `din6`, `din7`, `dout0`, `dout1`, `dout2`, `dout3`.

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

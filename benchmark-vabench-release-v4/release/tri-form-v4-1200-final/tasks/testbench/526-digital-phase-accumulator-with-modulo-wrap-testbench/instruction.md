# Digital Phase Accumulator With Modulo Wrap Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Digital Phase Accumulator With Modulo Wrap` DUT. The evaluator runs the same submitted bytes
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

- `P_TIMER_INCREMENT`: On every dt timer event, normalized phase advances by phase_step.
- `P_MODULO_WRAP`: The phase state wraps modulo one and never grows unbounded.
- `P_PHASE_RAIL_SCALING`: Phase_out equals wrapped normalized phase scaled by the local VDD-minus-VSS rail span.
- `P_PHASE_DERIVED_CLOCK`: Clk_out is rail-high while normalized phase is below 0.5 and low while phase is at or above 0.5.
- `P_PARAMETERIZED_PERIOD`: Changing dt or phase_step changes the observable phase and clock cadence according to the same update and wrap rules.

The required trace names are: `time`, `VDD`, `VSS`, `clk_out`, `phase_out`.

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

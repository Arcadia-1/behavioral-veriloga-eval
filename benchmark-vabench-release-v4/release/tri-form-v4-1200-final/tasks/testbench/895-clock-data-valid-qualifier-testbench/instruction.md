# Clock-and-data Valid Qualifier Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Clock-and-data Valid Qualifier` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: Reset or disable clears valid, qualification, and the public age metric.
- `P_DATA_EDGE_RESTART`: Either polarity data edge restarts the age count at zero while enabled.
- `P_CLOCKED_AGE`: Each later rising clk edge increments age before qualification.
- `P_INCLUSIVE_WINDOW`: Ages one through max_age_cycles are qualified and older ages are not.
- `P_REGISTERED_METRIC`: valid_out is the registered qualified state and the metric reports saturated normalized age.

The required trace names are: `time`, `clk`, `data`, `rst`, `enable`, `valid_out`, `edge_age_metric`, `qualified`.

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

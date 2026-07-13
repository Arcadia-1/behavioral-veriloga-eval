# Final Step File Metric Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Final Step File Metric` DUT. The evaluator runs the same submitted bytes
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

- `P_ZERO_INITIAL_STATE`: Before any qualifying ref edge, the event count and metric_out are zero.
- `P_RISING_EDGE_COUNT`: Every rising ref crossing through vth increments the retained event count exactly once; falling crossings do not.
- `P_NORMALIZED_METRIC`: Metric_out equals the VDD-to-VSS rail span multiplied by the retained event count divided by four.
- `P_EVENT_UPDATED_OUTPUT`: Metric_out changes only after counted rising events and uses finite transition smoothing of the retained target.
- `P_FINAL_TEXT_RECORD`: At final_step, the module emits one text metric record to candidate.out in the simulator working directory with format count=<integer> metric=<fixed-point to three decimals>.

The required trace names are: `time`, `vdd`, `vss`, `ref`, `metric_out`.

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

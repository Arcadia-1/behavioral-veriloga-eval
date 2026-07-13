# Rail Normalized Metric Mapper Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Rail Normalized Metric Mapper` DUT. The evaluator runs the same submitted bytes
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

- `P_NORMALIZE_MEAS_RELATIVE_TO_THE_LOCAL`: Normalize meas relative to the local V(vdd,vss) span and vss rail.
- `P_CLIP_THE_NORMALIZED_METRIC_TO_THE`: Clip the normalized metric to the public voltage-coded range.
- `P_ASSERT_VALID_ONLY_WHEN_ENABLE_IS`: Assert valid only when enable is high, supply span is valid, and the measurement lies inside the local rail window.
- `P_CLEAR_NORM_AND_VALID_WHILE_DISABLED`: Clear norm and valid while disabled or under the minimum supply span.
- `P_USE_LOCAL_ANALOG_HELPER_FUNCTIONS_RATHER`: Use local analog helper functions rather than user task/endtask syntax.

The required trace names are: `time`, `meas`, `vdd`, `vss`, `en`, `norm`, `valid`.

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

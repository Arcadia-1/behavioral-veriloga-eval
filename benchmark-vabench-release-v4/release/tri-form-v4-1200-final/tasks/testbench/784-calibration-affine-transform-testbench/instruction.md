# Calibration Affine Transform Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Calibration Affine Transform` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_EACH_RISING_CLOCK_CROSSING_COMPUTE`: On each rising clock crossing, compute a local affine calibration transform from raw, gain_ctrl, and offset_ctrl while reset is low and enable is high.
- `P_MAP_GAIN_CTRL_TO_A_PUBLIC`: Map gain_ctrl to a public gain range and offset_ctrl to a centered offset.
- `P_CLEAR_OUTPUT_AND_METRIC_WHILE_RESET`: Clear output and metric while reset is high or enable is low; otherwise clip the transformed output into the public voltage-coded range.
- `P_EXPOSE_A_BOUNDED_RESIDUAL_METRIC_FOR`: Expose a bounded residual metric for the transform magnitude.
- `P_USE_LOCAL_ANALOG_HELPER_FUNCTIONS_RATHER`: Use local analog helper functions rather than user task/endtask syntax.

The required trace names are: `time`, `clk`, `en`, `gain_ctrl`, `offset_ctrl`, `out`, `raw`, `resid_metric`, `rst`.

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

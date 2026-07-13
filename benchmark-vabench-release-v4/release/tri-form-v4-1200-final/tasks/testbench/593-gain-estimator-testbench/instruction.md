# Gain Estimator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Gain Estimator` DUT. The evaluator runs the same submitted bytes
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

- `P_START_TIME_GATING`: Samples before start_time do not contribute to measured input or output extrema and valid remains low.
- `P_PERIODIC_EXTREMA`: At each sample_period after start_time, the estimator updates minima and maxima of the input and output differential voltages.
- `P_VALIDITY_THRESHOLD`: Valid remains rail-low until the observed input differential span exceeds min_input_span and remains rail-high afterwards.
- `P_SPAN_RATIO`: Once valid, the measured gain equals output differential span divided by input differential span.
- `P_NORMALIZED_GAIN_OUTPUT`: Gain_out equals the VDD-to-VSS rail span multiplied by measured gain divided by gain_scale.
- `P_EVENT_UPDATED_TARGETS`: Gain_out and valid reflect event-updated retained targets with finite smoothing rather than continuously varying transition inputs.

The required trace names are: `time`, `vdd`, `vss`, `vinp`, `vinn`, `voutp`, `voutn`, `gain_out`, `valid`.

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

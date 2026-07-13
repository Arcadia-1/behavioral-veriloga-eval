# LDO Regulator Macro Model Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `LDO Regulator Macro Model` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_AND_RESET_STATE`: Initialization or active-high reset sets out to 0.60 V and metric to 0.9 V.
- `P_LOAD_TARGET`: At each eligible rising clock crossing, vin is clamped to 0 through 0.9 V and target equals 0.62 V minus 0.055 times that load.
- `P_FIRST_ORDER_REGULATION`: Out advances by 0.35 of the remaining target error on each eligible rising clock crossing.
- `P_REGULATED_OUTPUT_CLAMP`: The held output remains within 0.25 V through 0.75 V.
- `P_ERROR_METRIC`: Metric equals 0.9 V minus four times the absolute output-to-target error, clamped to 0 through 0.9 V.
- `P_CLOCKED_HOLD`: Out and metric hold between rising clock crossings except for transition smoothing.

The required trace names are: `time`, `clk`, `rst`, `vin`, `out`, `metric`.

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

# Bandgap Reference Macro Model Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Bandgap Reference Macro Model` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_AND_BROWNOUT`: Reset or vin below vstart forces out and metric to 0 V.
- `P_CLOCKED_FIRST_ORDER_SETTLING`: On eligible rising clock crossings, the held reference advances by 0.35 of the remaining error to the clamped line-corrected target.
- `P_TARGET_AND_OUTPUT_CLAMPS`: The line-corrected target is clamped to 0 through vin minus 0.05 V, and driven out remains within 0 through 0.9 V.
- `P_VALIDITY_ENCODING`: Metric is 0 V in reset or brownout, 0.2 V during startup below the 0.48 V validity threshold, and 0.9 V after the held reference exceeds it.
- `P_CLOCKED_HOLD`: Above startup, the reference state changes only on rising clock crossings and holds between samples.

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

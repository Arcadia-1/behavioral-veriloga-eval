# Bias Voltage Generator With Enable Trim Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Bias Voltage Generator With Enable Trim` DUT. The evaluator runs the same submitted bytes
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

- `P_CLOCKED_UPDATE`: Bias state changes are evaluated on rising clk crossings through vth and hold between clock updates.
- `P_DISABLE_RESET`: At an update, rst above vth or vin below 0.25 V disables the generator, returning out and metric to 0 V.
- `P_TRIM_TARGET`: When enabled, the target is 0.28 V plus 0.55 times (vin minus 0.25 V) divided by 0.65 V, clamped to 0.28 V through 0.82 V.
- `P_SETTLING`: At each enabled update, out advances by 45 percent of the remaining difference to the current target rather than jumping directly.
- `P_MONOTONIC_TRIM`: For otherwise equal enabled histories, a higher trim request produces a target and settled out value no lower than a smaller request.
- `P_ENABLE_METRIC`: metric approaches 0.9 V while enabled and 0 V while disabled, with transition smoothing set by tr.

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

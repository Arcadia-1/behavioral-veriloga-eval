# Current-limited Regulator Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Current-limited Regulator Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation drives vout, limit_metric, and regulation_ok low.
- `P_NORMAL_REGULATION`: With adequate headroom and sub-limit demand, vout equals vref and regulation_ok is asserted.
- `P_DROPOUT_CLAMP`: When input headroom is insufficient, vout is clamped to max(vss, vin minus dropout).
- `P_CURRENT_LIMITING`: Demand above demand_limit produces limit_metric equal to the overload and reduces vout by that overload subject to rails and dropout.
- `P_REGULATION_FLAG`: regulation_ok is high only for enabled, non-reset, non-limited operation with enough input headroom.

The required trace names are: `time`, `vin`, `load_demand`, `enable`, `rst`, `vout`, `limit_metric`, `regulation_ok`.

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

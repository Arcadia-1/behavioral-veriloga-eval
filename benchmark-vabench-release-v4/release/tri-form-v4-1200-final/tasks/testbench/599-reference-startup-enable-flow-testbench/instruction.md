# Reference Startup Enable Flow Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Reference Startup Enable Flow` DUT. The evaluator runs the same submitted bytes
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

- `P_SUPPLY_AND_ENABLE_MONITORS`: Supply_ok is 0.9 V exactly when vdd_in exceeds 0.32 V, while enable_mon is 0.9 V exactly when en exceeds vth.
- `P_RESET_OR_BROWNOUT`: Active reset or a bad supply clears out, metric, startup progress, and state; a supply dip also removes valid status.
- `P_DISABLED_REFERENCE`: With supply good and enable low, out is 0.05 V, metric is 0.1 V, startup progress is cleared, and state_mon represents state 1.
- `P_ENABLED_SETTLING`: On each rising clk crossing with supply good and enable high, out advances by 0.32 times its remaining error to 0.55 V and the startup count increments up to 8.
- `P_STARTUP_VALIDITY`: During enabled startup metric is 0.25 V and state is 2; after at least five enabled updates with out above 0.48 V, metric is 0.9 V and state is 3.
- `P_BROWNOUT_RECOVERY`: After a supply dip and restoration with enable asserted, the output and monitors repeat the same startup sequence before returning valid.

The required trace names are: `time`, `clk`, `rst`, `vdd_in`, `en`, `out`, `metric`, `supply_ok`, `enable_mon`, `state_mon`, `startup_mon`.

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

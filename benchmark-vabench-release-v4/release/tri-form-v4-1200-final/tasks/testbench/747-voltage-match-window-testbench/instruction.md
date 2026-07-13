# Voltage Match Window Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Voltage Match Window` DUT. The evaluator runs the same submitted bytes
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

- `P_COMPARE_THE_ANALOG_VOLTAGE_DIFFERENCE_DIRECTLY`: Compare the analog voltage difference directly. Drive `vout` near `vh` when `abs(V(vin1) - V(vin2)) <= match_tol`; otherwise drive it near `0 V`. The decision should be deterministic and memoryless, with a smoothed voltage transition on the output.
- `P_MATCH_TOL_0_05_V_FROM`: `match_tol = 0.05 V from [0:inf)`: maximum allowed absolute input difference for a match.
- `P_VH_0_9_V_MATCH_OUTPUT`: `vh = 0.9 V`: match output level.
- `P_TR_20_PS_FROM_0_INF`: `tr = 20 ps from [0:inf)`: output transition smoothing time.
- `P_MATCH_TOL_0_05_V_FROM_2`: - `match_tol = 0.05 V from [0:inf)`: maximum allowed absolute input difference for a match. - `vh = 0.9 V`: match output level. - `tr = 20 ps from [0:inf)`: output transition smoothing time.
- `P_USE_DETERMINISTIC_VOLTAGE_DOMAIN_VERILOG_A`: Use deterministic voltage-domain Verilog-A and voltage contributions only. Do not emit a testbench, checker logic, out-of-band test hooks, hard-code testbench sample points, use current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

The required trace names are: `time`, `vin1`, `vin2`, `vout`.

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

# Bandgap Startup and Trim System Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Bandgap Startup and Trim System` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_BROWNOUT_CLEAR`: On reset or brownout below POR, clear trim code, ready, error metric, and drive vref low.
- `P_POR_STARTUP`: Enable the reference only after vdd_sense remains above vpor for two consecutive rising clock edges.
- `P_CORE_REFERENCE`: Generate a behavioral PTAT/CTAT reference metric from temp_proxy around vref_nom.
- `P_TRIM_SEARCH`: When trim_req is high, update the 4-bit trim code once per rising clock edge to reduce reference error.
- `P_READY_QUALIFICATION`: Assert ready only after three consecutive enabled updates with error magnitude within ready_tol.

The required trace names are: `time`, `vdd_sense`, `clk`, `rst`, `trim_req`, `temp_proxy`, `vref`, `trim_3`, `trim_2`, `trim_1`, `trim_0`, `ready`, `error_metric`.

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

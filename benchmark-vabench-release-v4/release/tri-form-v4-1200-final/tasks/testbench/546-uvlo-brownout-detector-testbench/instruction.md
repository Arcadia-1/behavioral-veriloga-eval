# UVLO Brownout Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `UVLO Brownout Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_FAULT`: Active reset clears the power-good out signal and drives metric to the public fault code 0.9 V.
- `P_UPPER_TRIP_ASSERT`: On a sampled update, vin strictly greater than 0.65 V asserts power-good out.
- `P_HYSTERESIS_HOLD`: For sampled vin values from 0.55 V through 0.65 V inclusive, out preserves its previous power-good state.
- `P_BROWNOUT_CLEAR`: On a sampled update, vin strictly less than 0.55 V clears out to the brownout state.
- `P_STATUS_DISTINCTION`: Metric is the checker-observable status code: 0.1 V when out is power-good high and 0.9 V when reset, undervoltage, or brownout is active.

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

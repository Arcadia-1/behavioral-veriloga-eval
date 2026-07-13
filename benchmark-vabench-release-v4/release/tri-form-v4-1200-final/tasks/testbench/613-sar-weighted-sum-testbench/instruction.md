# SAR Weighted Sum Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `SAR Weighted Sum` DUT. The evaluator runs the same submitted bytes
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

- `P_THRESHOLD_DECODE`: Each D input contributes logic 1 only while its voltage is strictly above vth; a value at or below vth contributes logic 0.
- `P_WEIGHT_ORDER`: The decoded contribution order is D10 at seven-eighths full scale, D9 at one-half, D8 at one-quarter, a 5:3 split across D7 and D6, then a binary tail from D5 through D0.
- `P_BIPOLAR_ENDPOINTS`: All decision inputs low produce -1 V, while all decision inputs high produce one 512-unit step below +1 V on the normalized bipolar scale.
- `P_MONOTONIC_CODE_WEIGHT`: Changing any decoded decision from low to high without lowering another decision cannot decrease VOUT.
- `P_CONTINUOUS_DECODE`: VOUT continuously reflects the current threshold-decoded input combination without a clock, reset, or retained code state.

The required trace names are: `time`, `d10`, `d9`, `d8`, `d7`, `d6`, `d5`, `d4`, `d3`, `d2`, `d1`, `d0`, `vout`.

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

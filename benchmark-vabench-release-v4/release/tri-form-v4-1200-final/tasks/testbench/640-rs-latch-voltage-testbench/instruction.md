# RS Latch Voltage Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `RS Latch Voltage` DUT. The evaluator runs the same submitted bytes
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

- `P_LOGIC_THRESHOLDS_OUTPUT_AMPLITUDE`: Interpret set and reset as logic high above 0.45 V and drive outputs with 0.9 V high and 0.0 V low levels.
- `P_SET_RESET_PRIORITY`: A set-only input drives Q high, and a reset-only input drives Q low.
- `P_HOLD_STATE`: When neither set-only nor reset-only is asserted, preserve the previous Q state after initializing Q low.
- `P_QBAR_COMPLEMENT`: Drive `vout_qbar` as the logical complement of Q.

The required trace names are: `time`, `vin_r`, `vin_s`, `vout_q`, `vout_qbar`.

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

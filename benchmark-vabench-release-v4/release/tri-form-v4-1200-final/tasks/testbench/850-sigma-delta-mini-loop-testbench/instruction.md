# Sigma-delta Modulator Mini Loop Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Sigma-delta Modulator Mini Loop` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_CLEAR`: Reset clears the loop state, output bit, and decimator result.
- `P_FEEDBACK_STATE_UPDATE`: Each rising clock edge updates the bounded integrator from VIN and the previous feedback bit.
- `P_COMPARATOR_DECISION`: The output bit reflects the updated state relative to VCM.
- `P_DECIMATOR_WINDOW`: The four-bit result reports the saturated high-bit count for each complete 16-sample window.
- `P_STATE_BOUNDED`: The public state metric remains within the configured state limit.

The required trace names are: `time`, `vin`, `clk`, `rst`, `bit_out`, `avg_3`, `avg_2`, `avg_1`, `avg_0`, `state_metric`.

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

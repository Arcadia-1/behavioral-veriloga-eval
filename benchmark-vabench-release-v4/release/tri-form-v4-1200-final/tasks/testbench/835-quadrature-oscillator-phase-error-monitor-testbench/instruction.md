# Quadrature Oscillator Phase-error Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Quadrature Oscillator Phase-error Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear phase metric, status, and `valid`.
- `P_TRACK_RISING_THRESHOLD_CROSSINGS_OF_CLK`: Track rising threshold crossings of `clk_i` and `clk_q`.
- `P_ESTIMATE_A_VOLTAGE_DOMAIN_PHASE_ERROR`: Estimate a voltage-domain phase-error metric from the relative event order and interval proxy.
- `P_ASSERT_QUADRATURE_OK_WHEN_THE_MEASURED`: Assert `quadrature_ok` when the measured phase proxy stays within `phase_tol` for two cycles.
- `P_ASSERT_VALID_AFTER_BOTH_I_AND`: Assert `valid` after both I and Q edges have been observed.

The required trace names are: `time`, `clk_i`, `clk_q`, `rst`, `enable`, `phase_error_metric`, `quadrature_ok`, `valid`.

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

# Polyphase I/Q Balance Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Polyphase I/Q Balance Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive outputs to `vcm` and clear metrics.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, sample I and Q input deviations around `vcm`.
- `P_DRIVE_CORRECTED_I_Q_OUTPUTS_WITH`: Drive corrected I/Q outputs with bounded amplitude normalization.
- `P_EXPOSE_AMPLITUDE_AND_PHASE_ERROR_PROXIES`: Expose amplitude and phase-error proxies as separate voltage-domain metrics.
- `P_ASSERT_BALANCED_ONLY_WHEN_BOTH_METRICS`: Assert `balanced` only when both metrics remain below their thresholds for two updates.

The required trace names are: `time`, `i_in`, `q_in`, `clk`, `rst`, `enable`, `i_out`, `q_out`, `amp_error_metric`, `phase_error_metric`, `balanced`.

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

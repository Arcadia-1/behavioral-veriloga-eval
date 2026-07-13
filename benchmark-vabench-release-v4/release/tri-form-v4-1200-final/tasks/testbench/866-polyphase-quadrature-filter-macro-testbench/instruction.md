# Polyphase Quadrature Filter Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Polyphase Quadrature Filter Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_ENABLE_IS`: On reset or when `enable` is low, clear path states, metrics, `valid`, and drive outputs to `vcm`.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, update an in-phase sampled state from `vin`.
- `P_UPDATE_A_QUADRATURE_SAMPLED_STATE_USING`: Update a quadrature sampled state using the previous in-phase state so the Q output is phase-shifted relative to I.
- `P_DRIVE_I_OUT_AND_Q_OUT`: Drive `i_out` and `q_out` around `vcm` from the two path states.
- `P_REPORT_A_BOUNDED_PHASE_ORDER_METRIC`: Report a bounded phase/order metric on `phase_metric` and an amplitude-balance metric on `amp_metric`.
- `P_ASSERT_VALID_AFTER_AT_LEAST_FOUR`: Assert `valid` after at least four enabled sample updates.

The required trace names are: `time`, `vin`, `clk`, `rst`, `enable`, `i_out`, `q_out`, `amp_metric`, `phase_metric`, `valid`.

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

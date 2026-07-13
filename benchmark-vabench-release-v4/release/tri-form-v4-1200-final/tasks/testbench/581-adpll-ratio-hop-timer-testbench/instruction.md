# ADPLL Ratio Hop Timer Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `ADPLL Ratio Hop Timer` DUT. The evaluator runs the same submitted bytes
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

- `P_RATIO_REQUEST_CLAMP`: The voltage-coded ratio request rounds V(ratio_ctrl) to the nearest integer with half-step boundaries and then clips the feedback divide ratio to the inclusive ratio_min through ratio_max range, including legal non-default override ranges.
- `P_DCO_FREQUENCY_BOUNDS`: The behavioral DCO on vout remains within the configured f_min and f_max limits.
- `P_FEEDBACK_DERIVED_FROM_DCO`: Feedback-clock activity is derived by dividing vout activity by the requested ratio rather than from an independent clock source.
- `P_BOUNDED_CONTROL_MONITOR`: Reference-versus-feedback timing error adjusts a bounded control state represented by rail-referenced vctrl_mon.
- `P_PRE_HOP_LOCK`: Stable pre-hop tracking produces lock only after lock_count_target consecutive feedback events satisfy lock_tol.
- `P_RATIO_HOP_REACQUISITION`: A changed ratio request causes loss of lock qualification followed by renewed lock after the loop tracks the new feedback cadence.

The required trace names are: `time`, `vdd`, `vss`, `ref_clk`, `ratio_ctrl`, `fb_clk`, `vout`, `vctrl_mon`, `lock`.

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

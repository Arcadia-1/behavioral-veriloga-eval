# Two-stage Op-amp Slew Macromodel Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Two-stage Op-amp Slew Macromodel` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_ENABLE_IS`: On reset or when `enable` is low, drive `vout` and `stage1_metric` to `vcm`, clear `slew_metric`, `clamp_flag`, and `settled`.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, sample the differential input `vinp - vinn`.
- `P_COMPUTE_A_FIRST_STAGE_METRIC_FROM`: Compute a first-stage metric from the sampled differential input, centered around `vcm` and limited to `[vss, vdd]`.
- `P_COMPUTE_AN_OUTPUT_TARGET_FROM_THE`: Compute an output target from the first-stage metric and `stage2_gain`; `load_step` may request a bounded target perturbation around the same common-mode reference.
- `P_CLAMP_THE_OUTPUT_TARGET_TO_VSS`: Clamp the output target to `[vss, vdd]` and assert `clamp_flag` only when clamping occurs.
- `P_MOVE_VOUT_TOWARD_THE_CLAMPED_TARGET`: Move `vout` toward the clamped target by no more than `slew_step` per enabled clock edge.
- `P_ASSERT_SETTLED_ONLY_AFTER_TWO_CONSECUTIVE_UPDATES`: Assert `settled` only after the output error has remained within `settle_tol` for two consecutive enabled updates.

The required trace names are: `time`, `vinp`, `vinn`, `clk`, `rst`, `enable`, `load_step`, `vout`, `stage1_metric`, `slew_metric`, `clamp_flag`, `settled`.

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

# Two-stage Op-amp Slew Macromodel Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `two_stage_opamp_slew_macromodel.va`: `two_stage_opamp_slew_macromodel`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_ENABLE_IS`: On reset or when `enable` is low, drive `vout` and `stage1_metric` to `vcm`, clear `slew_metric`, `clamp_flag`, and `settled`.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, sample the differential input `vinp - vinn`.
- `P_COMPUTE_A_FIRST_STAGE_METRIC_FROM`: Compute a first-stage metric from the sampled differential input, centered around `vcm` and limited to `[vss, vdd]`.
- `P_COMPUTE_AN_OUTPUT_TARGET_FROM_THE`: Compute an output target from the first-stage metric and `stage2_gain`; `load_step` may request a bounded target perturbation around the same common-mode reference.
- `P_CLAMP_THE_OUTPUT_TARGET_TO_VSS`: Clamp the output target to `[vss, vdd]` and assert `clamp_flag` only when clamping occurs.
- `P_MOVE_VOUT_TOWARD_THE_CLAMPED_TARGET`: Move `vout` toward the clamped target by no more than `slew_step` per enabled clock edge.
- `P_ASSERT_SETTLED_ONLY_AFTER_TWO_CONSECUTIVE_UPDATES`: Assert `settled` only after the output error has remained within `settle_tol` for two consecutive enabled updates.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `two_stage_opamp_slew_macromodel.va`.
Every supplied `.va` file is editable; do not add or omit files.

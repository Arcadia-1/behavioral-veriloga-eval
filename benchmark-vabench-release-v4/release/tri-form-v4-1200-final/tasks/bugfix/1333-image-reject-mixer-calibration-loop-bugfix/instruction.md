# Image-reject Mixer Calibration Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `image_reject_mixer_cal_loop_top.va`: `image_reject_mixer_cal_loop_top`
- `quadrature_mixer_proxy.va`: `quadrature_mixer_proxy`
- `image_cal_controller.va`: `image_cal_controller`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear outputs, image metric, and `calibrated`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, sample RF and quadrature LO inputs as voltage-domain mixer proxies.
- `P_GENERATE_I_AND_Q_OUTPUTS_USING`: Generate I and Q outputs using opposite LO polarities.
- `P_UPDATE_A_SIMPLE_GAIN_PHASE_CORRECTION`: Update a simple gain/phase correction state to reduce the image metric.
- `P_ASSERT_CALIBRATED_AFTER_THREE_CONSECUTIVE_UPDA`: Assert `calibrated` after three consecutive updates with image metric below `image_tol`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `image_reject_mixer_cal_loop_top.va`, `quadrature_mixer_proxy.va`, `image_cal_controller.va`.
Every supplied `.va` file is editable; do not add or omit files.

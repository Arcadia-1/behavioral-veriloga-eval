# Image-reject Mixer Calibration Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `image_reject_mixer_cal_loop_top.va`: `image_reject_mixer_cal_loop_top`
- `quadrature_mixer_proxy.va`: `quadrature_mixer_proxy`
- `image_cal_controller.va`: `image_cal_controller`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear outputs, image metric, and `calibrated`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, sample RF and quadrature LO inputs as voltage-domain mixer proxies.
- `P_GENERATE_I_AND_Q_OUTPUTS_USING`: Generate I and Q outputs using opposite LO polarities.
- `P_UPDATE_A_SIMPLE_GAIN_PHASE_CORRECTION`: Update a simple gain/phase correction state to reduce the image metric.
- `P_ASSERT_CALIBRATED_AFTER_THREE_CONSECUTIVE_UPDA`: Assert `calibrated` after three consecutive updates with image metric below `image_tol`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `image_reject_mixer_cal_loop_top.va`, `quadrature_mixer_proxy.va`, `image_cal_controller.va`.
Do not add or omit artifacts.

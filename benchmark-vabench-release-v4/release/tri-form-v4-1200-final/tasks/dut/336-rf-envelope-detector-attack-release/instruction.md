# RF Envelope Detector with Attack/Release

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `rf_envelope_detector_attack_release.va`: `rf_envelope_detector_attack_release`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear envelope, metric, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, estimate input magnitude as distance from `vcm`.
- `P_USE_A_FASTER_ATTACK_STEP_WHEN`: Use a faster attack step when magnitude rises and a slower release step when it falls.
- `P_DRIVE_ENVELOPE_WITH_THE_TRACKED_MAGNITUDE`: Drive `envelope` with the tracked magnitude mapped into the public voltage range.
- `P_EXPOSE_WHETHER_THE_LAST_UPDATE_USED`: Expose whether the last update used attack or release on `attack_metric`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `rf_envelope_detector_attack_release.va`.
Do not add or omit artifacts.

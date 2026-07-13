# Foreground RDAC Calibrator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `foreground_rdac_calibrator.va`: `foreground_rdac_calibrator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_MSB_TRIAL_CODE`: At startup, calibration is active with `dc6` asserted and all lower RDAC bits deasserted.
- `P_CLOCKED_RDAC_DECISION_SEQUENCE`: On each rising `ck` crossing while active, resolve the current trial bit from `d` versus `vth` and advance from MSB to LSB.
- `P_DECISION_POLARITY`: Comparator-low and comparator-high decisions update the trial bit in the declared polarity without inverting the search direction.
- `P_CALIBRATION_COMPLETION`: After the final RDAC decision, deassert calibration enable and hold the completed code.
- `P_RDAC_OUTPUT_LEVELS`: All RDAC code and enable outputs remain voltage-coded at valid low/high levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `foreground_rdac_calibrator.va`.
Do not add or omit artifacts.

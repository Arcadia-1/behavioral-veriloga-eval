# RS Phase Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `rs_phase_detector.va`: `rs_phase_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DETECT_RISING_REF_AND_FB_CROSSINGS`: Detect rising `ref` and `fb` crossings at `vdd/2`.
- `P_A_RISING_REF_EDGE_SETS_THE`: A rising `ref` edge sets the latch state so `up` is high and `down` is low.
- `P_A_RISING_FB_EDGE_RESETS_THE`: A rising `fb` edge resets the latch state so `up` is low and `down` is high.
- `P_HOLD_THE_MOST_RECENT_LATCH_STATE`: Hold the most recent latch state between qualifying input edges.
- `P_INITIALIZE_TO_THE_RESET_STATE_WITH`: Initialize to the reset state with `up` low and `down` high.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `rs_phase_detector.va`.
Do not add or omit artifacts.

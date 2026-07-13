# PFD Up Down State

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pfd_up_down_state.va`: `pfd_up_down_state`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DETECT_RISING_REF_AND_FB_CROSSINGS`: Detect rising `ref` and `fb` crossings at `vdd/2`.
- `P_MAINTAIN_AN_INTEGER_DETECTOR_STATE_BOUNDED`: Maintain an integer detector state bounded to `-1`, `0`, or `+1`.
- `P_A_RISING_REF_EDGE_INCREMENTS_THE`: A rising `ref` edge increments the state up to `+1`.
- `P_A_RISING_FB_EDGE_DECREMENTS_THE`: A rising `fb` edge decrements the state down to `-1`.
- `P_DRIVE_UP_HIGH_WHEN_THE_STATE`: Drive `up` high when the state is `+1`.
- `P_DRIVE_DOWN_HIGH_WHEN_THE_STATE`: Drive `down` high when the state is `-1`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pfd_up_down_state.va`.
Do not add or omit artifacts.

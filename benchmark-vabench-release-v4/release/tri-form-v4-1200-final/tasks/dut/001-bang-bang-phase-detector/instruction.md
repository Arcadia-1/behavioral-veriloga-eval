# Bang-Bang Phase Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `bbpd_ref.va`: `bbpd_ref`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DIRECTION`: Each data transition selects UP for clock-high/retimed-low, DOWN for clock-low/retimed-high, and neither otherwise.
- `P_MUTUAL_EXCLUSION`: UP and DOWN are never asserted simultaneously.
- `P_PULSE_CLEAR`: An asserted correction output returns low after the next clock transition.
- `P_RAIL_LEVELS`: Asserted outputs approach vdd and inactive outputs approach 0 V with finite smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `bbpd_ref.va`.
Do not add or omit artifacts.

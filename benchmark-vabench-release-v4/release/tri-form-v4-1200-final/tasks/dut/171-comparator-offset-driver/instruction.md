# Comparator Offset Driver

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `comparator_offset_binary_driver.va`: `comparator_offset_binary_driver`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FALLING_CLOCK_DECISION_SAMPLE`: On each falling `clk` threshold crossing, sample `dcmpp` to choose the next binary-search direction.
- `P_DECISION_POLARITY_UPDATE`: A high decision moves the differential input negative and a low decision moves it positive.
- `P_HALVING_SEARCH_STEP`: The differential search step halves after each sampled decision.
- `P_COMMON_MODE_HALF_SCALE_DRIVE`: `vinp` and `vinn` are driven symmetrically around the common-mode level with half differential amplitude on each side.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `comparator_offset_binary_driver.va`.
Do not add or omit artifacts.

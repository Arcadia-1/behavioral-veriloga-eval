# Three Way Threshold Mux

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `three_way_threshold_mux.va`: `three_way_threshold_mux`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DIFFERENTIAL_CONTROL`: Use `V(cntrlp, cntrlm)` as the mux control signal.
- `P_LOW_REGION_SELECTS_SIGIN1`: When control is below `sigth_low`, drive `sigout` from `sigin1`.
- `P_MIDDLE_REGION_SELECTS_SIGIN2`: When control is in the inclusive window `[sigth_low, sigth_high]`, drive `sigout` from `sigin2`.
- `P_HIGH_REGION_SELECTS_SIGIN3`: When control is above `sigth_high`, drive `sigout` from `sigin3`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `three_way_threshold_mux.va`.
Do not add or omit artifacts.

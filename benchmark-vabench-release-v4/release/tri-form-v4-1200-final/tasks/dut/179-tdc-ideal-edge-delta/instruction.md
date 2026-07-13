# TDC Ideal Edge Delta

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `tdc_ideal_edge_delta.va`: `tdc_ideal_edge_delta`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SAMPLE_REARMS_MEASUREMENT`: At initialization and each rising `samp` crossing, input trigger flags clear while the previous output is retained until a new edge pair is measured.
- `P_INPUT_EDGE_PAIR_CAPTURE`: A measurement completes only after the required `inp` and `inn` rising-edge pair has been observed.
- `P_SIGNED_DELTA_POLARITY`: `vout` represents the `inp` minus `inn` edge-time delta with the specified polarity.
- `P_FULL_RANGE_SCALE`: The reported timing delta uses the specified full-range scale rather than a half-range or alternate denominator.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `tdc_ideal_edge_delta.va`.
Do not add or omit artifacts.

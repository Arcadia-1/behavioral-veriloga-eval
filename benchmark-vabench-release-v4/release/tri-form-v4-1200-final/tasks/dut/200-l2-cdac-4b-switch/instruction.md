# L2 CDAC 4b Switch

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `l2_cdac_4b_switch.va`: `l2_cdac_4b_switch`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FIRST_READY_EDGE_ARMS_ONLY`: The first rising `rdy` edge arms the DAC and leaves the initialized output at zero.
- `P_READY_SAMPLES_FOUR_BITS`: Each later rising `rdy` edge samples `din1..din4` against `vth` with the declared switched weights.
- `P_SWITCHED_WEIGHT_DENOMINATOR`: Compute `switched_weight` and normalize by `8.5` before output scaling.
- `P_BIPOLAR_CDAC_OUTPUT`: Map the sampled ratio to `(switched_weight / 8.5) * 2.0 * vdd - vdd` and hold it between ready edges.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `l2_cdac_4b_switch.va`.
Do not add or omit artifacts.

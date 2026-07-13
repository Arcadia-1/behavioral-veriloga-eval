# First Order Sigma Delta Modulator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `first_order_sigma_delta_modulator.va`: `first_order_sigma_delta_modulator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RISING_EDGE_UPDATE`: The one-bit output state updates only from accumulator decisions made on rising crossings of vclk through vth_clk.
- `P_FIRST_ORDER_FEEDBACK`: Each clocked decision reflects accumulation of the current normalized input minus the previous one-bit feedback state.
- `P_BINARY_OUTPUT`: bitout is voltage-coded low near 0 V or high near vh with finite transition smoothing.
- `P_INPUT_DENSITY_ORDER`: Over a sufficiently long common observation interval, a larger constant vin produces a nondecreasing fraction of high output bits.
- `P_FEEDBACK_STABILITY`: For an in-range constant input, the output stream continues to alternate as needed rather than running away as an open-loop accumulator.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `first_order_sigma_delta_modulator.va`.
Do not add or omit artifacts.

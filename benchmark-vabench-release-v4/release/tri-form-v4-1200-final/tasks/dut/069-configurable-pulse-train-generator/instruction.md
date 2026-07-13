# Configurable Pulse Train Generator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `configurable_pulse_train.va`: `configurable_pulse_train`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_IDLE_CAPTURE`: A sampled high start while idle captures unsigned period3:period0, width3:width0, and count3:count0 on a rising clk crossing.
- `P_ZERO_CODE_MINIMUM`: A zero-coded period, width, or count is interpreted as one clock sample rather than zero.
- `P_PULSE_COUNT`: Each accepted command emits exactly the captured count number of pulses.
- `P_WIDTH_AND_PERIOD`: Each pulse remains high for the captured width in clock samples and pulse starts are separated by the captured period in clock samples.
- `P_COMPLETION`: After the final pulse completes, pulse is low and done is asserted.
- `P_OUTPUT_LEVELS`: pulse and done use 0 V and vdd levels with finite transition smoothing set by tr.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `configurable_pulse_train.va`.
Do not add or omit artifacts.

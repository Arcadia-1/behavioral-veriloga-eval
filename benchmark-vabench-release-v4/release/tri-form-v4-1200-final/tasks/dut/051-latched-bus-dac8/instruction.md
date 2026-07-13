# Latched Bus DAC8

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `latched_bus_dac8.va`: `latched_bus_dac8`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RISING_EDGE_CAPTURE`: Each rising crossing of vclk through vth captures the unsigned value of b[7:0].
- `P_HOLD_BETWEEN_EDGES`: vout retains the value from the most recent rising clock crossing despite input-bus changes between update edges.
- `P_ENDPOINTS`: Latched code 0 maps to 0 V and latched code 255 maps to vref.
- `P_BINARY_MONOTONICITY`: Increasing the latched unsigned code never decreases vout, with b7 as MSB and b0 as LSB.
- `P_OUTPUT_SMOOTHING`: vout approaches each newly latched target with finite transition smoothing set by tr.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `latched_bus_dac8.va`.
Do not add or omit artifacts.

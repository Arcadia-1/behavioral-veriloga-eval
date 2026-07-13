# Clocked Four Input Mux

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `clocked_four_input_mux.va`: `clocked_four_input_mux`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FALLING_EDGE_SAMPLE_HOLD`: Only falling `clks` crossings through `vth` update `dout`; between those events the last selected input value is held.
- `P_SELECT_BIT_DECODE`: `dsel0` is the LSB and `dsel1` is the MSB when selecting among `din0` through `din3`.
- `P_ALL_FOUR_INPUTS_REACHABLE`: All four data inputs can be selected and forwarded to `dout` according to the two-bit select code.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `clocked_four_input_mux.va`.
Do not add or omit artifacts.

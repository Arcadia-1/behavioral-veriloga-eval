# Clocked Mux4 Sampler

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `clocked_mux4_sampler.va`: `clocked_mux4_sampler`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_SELECTS_DIN0`: While `rst` is high, the selected channel and `dout` are forced to `din0`.
- `P_FALLING_CLOCK_UPDATE_SAMPLE`: On each falling `clks` crossing with reset inactive and `update` high, latch `dsel0/dsel1` and sample the selected input.
- `P_UPDATE_LOW_HOLDS_STATE`: On falling `clks` crossings with `update` low, hold the previous selection and output value.
- `P_SELECT_DECODE_AND_OUTPUT_TIMING`: The held two-bit selection maps to `din0..din3` in binary order and drives `dout` with the declared transition timing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `clocked_mux4_sampler.va`.
Do not add or omit artifacts.

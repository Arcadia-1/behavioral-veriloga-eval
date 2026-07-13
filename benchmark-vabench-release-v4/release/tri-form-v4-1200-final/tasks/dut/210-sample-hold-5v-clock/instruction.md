# Sample Hold 5v Clock

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sample_hold_5v_clock.va`: `sample_hold_5v_clock`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DETECT_RISING_CROSSINGS_OF_VCLK_THROUGH`: Detect rising crossings of `vclk` through `vtrans_clk`. At each qualifying edge, sample the instantaneous value of `vin` and hold that sampled value on `vout` until the next rising clock edge. Falling clock edges must not update the held value.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sample_hold_5v_clock.va`.
Do not add or omit artifacts.

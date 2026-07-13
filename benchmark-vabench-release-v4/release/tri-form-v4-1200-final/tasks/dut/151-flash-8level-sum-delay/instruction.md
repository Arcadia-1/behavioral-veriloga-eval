# Flash 8level Sum Delay

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `flash_8level_sum_delay.va`: `flash_8level_sum_delay`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_FLASH_THRESHOLD_SUM`: Each rising `clks` crossing compares `V(vip,vim)` against the symmetric flash thresholds and updates `doutsum`.
- `P_REFERENCE_SCALING`: The flash thresholds use `V(refp)-V(refn)` multiplied by `ref_scaling`.
- `P_ONE_CYCLE_DELAYED_SUM`: `doutsumdelay` reports the previous sampled flash summary, not the current summary.
- `P_NORMALIZED_OUTPUT`: The flash summary is normalized by the eight-level count before being driven.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `flash_8level_sum_delay.va`.
Do not add or omit artifacts.

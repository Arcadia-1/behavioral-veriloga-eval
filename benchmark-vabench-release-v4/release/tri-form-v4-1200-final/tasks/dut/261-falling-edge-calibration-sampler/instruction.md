# Falling Edge Calibration Sampler

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `falling_edge_calibration_sampler.va`: `falling_edge_calibration_sampler`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span. Let `span = V(vdd, vss)` and treat the row as valid only when `V(en) > vth` and `span_min <= span <= span_max`. If `span` is below `0.05 V`, use `0.05 V` as the normalization span. Define `clip01(y)` as `y` limited to the range `[0, 1]` and `x0..x3 = clip01((V(inN) - V(vss)) / span)`.
- `P_INITIALIZE_OUT_FLAG_AND_METRIC_TO`: Initialize `out`, `flag`, and `metric` to `0 V`. On a falling edge of `clk`, clear all observables when `rst` is high or the row is not valid. Otherwise sample the comparison `x0 > x1`: drive `out = vhi` for true and `out = 0 V` for false, drive `flag` to the same value as `out`, and drive `metric = vhi * clip01(abs(x0 - x1))`. Hold the last observable values between falling clock edges, except that a reset assertion clears them.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `falling_edge_calibration_sampler.va`.
Do not add or omit artifacts.

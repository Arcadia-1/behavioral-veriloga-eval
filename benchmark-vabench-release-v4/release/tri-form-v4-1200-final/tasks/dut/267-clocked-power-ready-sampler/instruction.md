# Clocked Power Ready Sampler

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `clocked_power_ready_sampler.va`: `clocked_power_ready_sampler`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span. Let `span = V(vdd, vss)` and treat the row as valid only when `V(en) > vth` and `span_min <= span <= span_max`. If `span` is below `0.05 V`, use `0.05 V` as the normalization span. Define `clip01(y)` as `y` limited to the range `[0, 1]` and `x0..x3 = clip01((V(inN) - V(vss)) / span)`.
- `P_INITIALIZE_THE_READY_COUNT_AND_ALL`: Initialize the ready count and all observables to `0 V`. On a rising crossing of `clk` or a rising crossing of `rst`, clear the count and all observables when `rst` is high or the row is not valid. Otherwise, increment a saturating count by one up to a maximum of `4` when both `x0 > 0.25` and `x1 > 0.20`; if that sampled condition is not met, clear the count to zero. Drive `out = vhi * clip01(count / 4.0)`, assert `flag = vhi` when `count >= 3`, and drive `metric = vhi * clip01(abs(x0 - x1))`. Hold the last observable values between update events.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `clocked_power_ready_sampler.va`.
Do not add or omit artifacts.

# Dynamic Supply Enable Driver

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `dynamic_supply_enable_driver.va`: `dynamic_supply_enable_driver`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span. Let `span = V(vdd, vss)` and treat the row as valid only when `V(en) > vth` and `span_min <= span <= span_max`; otherwise drive `out`, `flag`, and `metric` to `0 V`. If `span` is below `0.05 V`, use `0.05 V` as the normalization span. Define `clip01(y)` as `y` limited to the range `[0, 1]`, `x0 = clip01((V(in0) - V(vss)) / span)`, and `c1 = clip01(V(ctrl1) / vhi)`.
- `P_COMPUTE_CORE_0_76_X0_0`: Compute `core = 0.76 * x0 + 0.18 * c1 + 0.12` and drive `out = vhi * clip01(core)` while valid. Assert `flag = vhi` when the local supply span is at least `0.78 V`, otherwise drive `flag = 0 V`. Drive `metric = vhi * clip01(abs((V(in0) - V(vss)) - 0.5 * span) / span)` as the bounded distance from the half-span input point.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `dynamic_supply_enable_driver.va`.
Do not add or omit artifacts.

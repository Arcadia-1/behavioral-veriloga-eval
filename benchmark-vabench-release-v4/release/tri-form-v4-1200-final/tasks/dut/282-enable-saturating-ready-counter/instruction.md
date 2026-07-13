# Enable Saturating Ready Counter

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `enable_saturating_ready_counter.va`: `enable_saturating_ready_counter`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span. Let `span = V(vdd, vss)` and treat the row as valid only when `V(en) > vth` and `span_min <= span <= span_max`. If `span` is below `0.05 V`, use `0.05 V` as the normalization span. Define `clip01(y)` as `y` limited to the range `[0, 1]` and `x0..x3 = clip01((V(inN) - V(vss)) / span)`.
- `P_INITIALIZE_A_SAMPLED_READY_COUNT_TO`: Initialize a sampled ready count to zero. On a rising edge of `clk` or on reset assertion, clear the count and all observables when `rst` is high or the row is not valid. Otherwise, increment the count by one and saturate it at `4.0` when `x0 > 0.25` and `x1 > 0.20`; clear the count to zero when either condition is not met. After the update, drive `out = vhi * clip01(count / 4.0)`, assert `flag = vhi` when `count >= 3.0`, otherwise drive `flag = 0 V`, and drive `metric = vhi * clip01(abs(x0 - x1))`. Hold the last observable values between update events.
- `P_BUILD_A_VOLTAGE_DOMAIN_ANALOG_MIXED`: Build a voltage-domain analog/mixed-signal helper or monitor. Enable-qualified saturating ready counter for power/reference settling flows.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for voltage-coded controls.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for output observables.
- `P_SPAN_MIN_0_62_V_SPAN`: `span_min = 0.62 V`, `span_max = 1.28 V`: legal local supply span measured as

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `enable_saturating_ready_counter.va`.
Do not add or omit artifacts.

# Clocked Power Ready Sampler Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `clocked_power_ready_sampler.va`: `clocked_power_ready_sampler`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span. Let `span = V(vdd, vss)` and treat the row as valid only when `V(en) > vth` and `span_min <= span <= span_max`. If `span` is below `0.05 V`, use `0.05 V` as the normalization span. Define `clip01(y)` as `y` limited to the range `[0, 1]` and `x0..x3 = clip01((V(inN) - V(vss)) / span)`.
- `P_INITIALIZE_THE_READY_COUNT_AND_ALL`: Initialize the ready count and all observables to `0 V`. On a rising crossing of `clk` or a rising crossing of `rst`, clear the count and all observables when `rst` is high or the row is not valid. Otherwise, increment a saturating count by one up to a maximum of `4` when both `x0 > 0.25` and `x1 > 0.20`; if that sampled condition is not met, clear the count to zero. Drive `out = vhi * clip01(count / 4.0)`, assert `flag = vhi` when `count >= 3`, and drive `metric = vhi * clip01(abs(x0 - x1))`. Hold the last observable values between update events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `clocked_power_ready_sampler.va`.
Every supplied `.va` file is editable; do not add or omit files.

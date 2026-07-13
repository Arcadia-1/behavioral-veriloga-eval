# Enable Qualified Bias Hold Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `enable_qualified_bias_hold.va`: `enable_qualified_bias_hold`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span. Let `span = V(vdd, vss)` and treat the row as valid only when `V(en) > vth` and `span_min <= span <= span_max`. If `span` is below `0.05 V`, use `0.05 V` as the normalization span. Define `clip01(y)` as `y` limited to the range `[0, 1]`, `x0..x3 = clip01((V(inN) - V(vss)) / span)`, and `c0 = clip01(V(ctrl0) / vhi)`.
- `P_INITIALIZE_THE_HELD_BIAS_OUTPUT_FLAG`: Initialize the held bias output, `flag`, and `metric` to `0 V`. On a rising edge of `clk`, clear all observables when `rst` is high or the row is not valid. Otherwise, when `c0 > 0.45`, update the held output to `out = vhi * clip01(0.70 * x0 + 0.30 * x1)` and assert `flag = vhi`. When `c0 <= 0.45`, hold the previous output value and drive `flag = 0 V`. After the update or hold decision, drive `metric = vhi * clip01(abs((out / vhi) - x2))`. Hold the last observable values between rising clock edges, except that a reset assertion clears them.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `enable_qualified_bias_hold.va`.
Every supplied `.va` file is editable; do not add or omit files.

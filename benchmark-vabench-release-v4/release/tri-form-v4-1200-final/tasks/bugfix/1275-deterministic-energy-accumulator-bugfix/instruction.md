# Deterministic Energy Accumulator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `deterministic_energy_accumulator.va`: `deterministic_energy_accumulator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span. Let `span = V(vdd, vss)` and treat the row as valid only when `V(en) > vth` and `span_min <= span <= span_max`. If `span` is below `0.05 V`, use `0.05 V` as the normalization span. Define `clip01(y)` as `y` limited to the range `[0, 1]`, `x0..x3 = clip01((V(inN) - V(vss)) / span)`, and `c0 = clip01(V(ctrl0) / vhi)`.
- `P_INITIALIZE_THE_ACCUMULATOR_STATE_AND_ALL`: Initialize the accumulator state and all observables to `0 V`. On a rising edge of `clk` or on reset assertion, clear the accumulator and all observables when `rst` is high or the row is not valid. Otherwise compute `aux = clip01(abs(x0 - x1) + 0.35 * c0)`, update `acc = clip01(0.62 * acc + 0.32 * aux)`, drive `out = vhi * acc`, assert `flag = vhi` when `acc > 0.58`, otherwise drive `flag = 0 V`, and drive `metric = vhi * aux`. Hold the last observable values between update events.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `deterministic_energy_accumulator.va`.
Every supplied `.va` file is editable; do not add or omit files.

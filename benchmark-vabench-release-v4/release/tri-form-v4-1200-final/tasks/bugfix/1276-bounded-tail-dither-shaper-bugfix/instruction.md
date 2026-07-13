# Bounded Tail Dither Shaper Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `bounded_tail_dither_shaper.va`: `bounded_tail_dither_shaper`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span `span = V(vdd, vss)`. Clear all observables when `en` is low or when `span` is outside `[span_min, span_max]`. The DUT updates its observable state on rising `clk` crossings and clears state while `rst` is high.
- `P_FOR_EACH_VALID_UPDATE_COMPUTE`: For each valid update, compute:
- `P_TEXT_X0_CLIP01_V_IN0_V`: ```text x0 = clip01((V(in0) - V(vss)) / span) x1 = clip01((V(in1) - V(vss)) / span) c0 = clip01(V(ctrl0) / vhi) aux = clip01(abs(x0 - x1) + 0.35*c0) acc = clip01(0.62*previous_acc + 0.32*aux) out = vhi*acc flag = vhi when acc > 0.58, otherwise 0 metric = vhi*aux ```
- `P_RESET_DISABLED_AND_OUT_OF_RANGE`: Reset, disabled, and out-of-range supply conditions set `previous_acc`, `out`, `flag`, and `metric` to 0. Preserve `in2`, `in3`, and `ctrl1` as public interface inputs; they are not part of the bounded-tail update formula for this task.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `bounded_tail_dither_shaper.va`.
Every supplied `.va` file is editable; do not add or omit files.

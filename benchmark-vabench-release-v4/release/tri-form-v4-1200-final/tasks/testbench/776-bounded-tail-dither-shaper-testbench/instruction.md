# Bounded Tail Dither Shaper Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Bounded Tail Dither Shaper` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span `span = V(vdd, vss)`. Clear all observables when `en` is low or when `span` is outside `[span_min, span_max]`. The DUT updates its observable state on rising `clk` crossings and clears state while `rst` is high.
- `P_FOR_EACH_VALID_UPDATE_COMPUTE`: For each valid update, compute:
- `P_TEXT_X0_CLIP01_V_IN0_V`: ```text x0 = clip01((V(in0) - V(vss)) / span) x1 = clip01((V(in1) - V(vss)) / span) c0 = clip01(V(ctrl0) / vhi) aux = clip01(abs(x0 - x1) + 0.35*c0) acc = clip01(0.62*previous_acc + 0.32*aux) out = vhi*acc flag = vhi when acc > 0.58, otherwise 0 metric = vhi*aux ```
- `P_RESET_DISABLED_AND_OUT_OF_RANGE`: Reset, disabled, and out-of-range supply conditions set `previous_acc`, `out`, `flag`, and `metric` to 0. Preserve `in2`, `in3`, and `ctrl1` as public interface inputs; they are not part of the bounded-tail update formula for this task.

The required trace names are: `time`, `clk`, `rst`, `in0`, `in1`, `in2`, `in3`, `ctrl0`, `ctrl1`, `vdd`, `vss`, `en`, `out`, `flag`, `metric`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.

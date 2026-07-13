# Deterministic Energy Accumulator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Deterministic Energy Accumulator` DUT. The evaluator runs the same submitted bytes
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

- `P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE`: Measure analog inputs relative to the local `vss` rail and normalize by the current local supply span. Let `span = V(vdd, vss)` and treat the row as valid only when `V(en) > vth` and `span_min <= span <= span_max`. If `span` is below `0.05 V`, use `0.05 V` as the normalization span. Define `clip01(y)` as `y` limited to the range `[0, 1]`, `x0..x3 = clip01((V(inN) - V(vss)) / span)`, and `c0 = clip01(V(ctrl0) / vhi)`.
- `P_INITIALIZE_THE_ACCUMULATOR_STATE_AND_ALL`: Initialize the accumulator state and all observables to `0 V`. On a rising edge of `clk` or on reset assertion, clear the accumulator and all observables when `rst` is high or the row is not valid. Otherwise compute `aux = clip01(abs(x0 - x1) + 0.35 * c0)`, update `acc = clip01(0.62 * acc + 0.32 * aux)`, drive `out = vhi * acc`, assert `flag = vhi` when `acc > 0.58`, otherwise drive `flag = 0 V`, and drive `metric = vhi * aux`. Hold the last observable values between update events.

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

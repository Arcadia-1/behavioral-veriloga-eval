# Programmable Gain Amplifier Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Programmable Gain Amplifier` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_UNITY`: While rst is active, the sampled gain is unity, out is vcm, and metric is low.
- `P_SAMPLED_GAIN_SELECT`: Each rising clk crossing with reset inactive samples gain_sel, selecting gain_high above vth and gain_low below vth; the selection holds between crossings.
- `P_COMMON_MODE_GAIN`: The unclamped output target is vcm plus the sampled gain times vin minus vcm.
- `P_OUTPUT_CLAMP`: Out is limited to the inclusive vmin through vmax range with finite smoothing.
- `P_CLIP_METRIC`: Metric is high exactly when the unclamped target lies outside vmin through vmax, and low otherwise; reset forces it low.

The required trace names are: `time`, `clk`, `rst`, `gain_sel`, `vin`, `out`, `metric`.

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

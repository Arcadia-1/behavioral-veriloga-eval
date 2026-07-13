# Reference Settling Window Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Reference Settling Window Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_EACH_RISING_CROSSING_OF_CLK`: On each rising crossing of `clk`, measure the absolute difference between `ref` and `target`. Drive `err_metric` as the clipped error magnitude scaled by `err_scale`. While reset is high, clear the settling counter and keep `valid` low. Otherwise, increment the counter on each in-window sample, clear it on any out-of-window sample, and assert `valid` only after `settle_cycles` consecutive in-window samples. Drive `settle_mon` as bounded progress from 0 to `vhi`. Smooth all outputs with `transition()`.
- `P_BUILD_A_MEASUREMENT_STYLE_BIAS_REFERENCE`: Build a measurement-style bias/reference monitor. The module samples a reference voltage against a target, reports the bounded error magnitude, and asserts validity only after consecutive in-window samples.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for `clk` and `rst`.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for voltage-coded outputs.
- `P_TOL_0_035_V_ALLOWED_ABSOLUTE`: `tol = 0.035 V`: allowed absolute error around `target`.
- `P_ERR_SCALE_0_20_V_ERROR`: `err_scale = 0.20 V`: error that maps to full-scale `err_metric`.

The required trace names are: `time`, `clk`, `err_metric`, `ref`, `rst`, `settle_mon`, `target`, `valid`.

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

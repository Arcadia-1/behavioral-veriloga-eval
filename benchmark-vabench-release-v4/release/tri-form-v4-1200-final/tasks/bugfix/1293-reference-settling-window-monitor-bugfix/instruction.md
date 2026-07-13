# Reference Settling Window Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `reference_settling_window_monitor.va`: `reference_settling_window_monitor`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_EACH_RISING_CROSSING_OF_CLK`: On each rising crossing of `clk`, measure the absolute difference between `ref` and `target`. Drive `err_metric` as the clipped error magnitude scaled by `err_scale`. While reset is high, clear the settling counter and keep `valid` low. Otherwise, increment the counter on each in-window sample, clear it on any out-of-window sample, and assert `valid` only after `settle_cycles` consecutive in-window samples. Drive `settle_mon` as bounded progress from 0 to `vhi`. Smooth all outputs with `transition()`.
- `P_BUILD_A_MEASUREMENT_STYLE_BIAS_REFERENCE`: Build a measurement-style bias/reference monitor. The module samples a reference voltage against a target, reports the bounded error magnitude, and asserts validity only after consecutive in-window samples.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for `clk` and `rst`.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for voltage-coded outputs.
- `P_TOL_0_035_V_ALLOWED_ABSOLUTE`: `tol = 0.035 V`: allowed absolute error around `target`.
- `P_ERR_SCALE_0_20_V_ERROR`: `err_scale = 0.20 V`: error that maps to full-scale `err_metric`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `reference_settling_window_monitor.va`.
Every supplied `.va` file is editable; do not add or omit files.

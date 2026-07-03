# Complete Calibration Loop

## Task Contract

- Form: `dut`
- Level: `L2`
- Category: Calibration, Trim, and DEM Control
- Base function: closed calibration loop
- Domain: `voltage`
- Target artifact(s): `complete_calibration_loop.va`
- Output boundary: implement only the requested DUT artifact; validation harnesses and simulator-private hooks are external to the requested output.

## Form-Specific Requirements

- Return exactly one Verilog-A source file named `complete_calibration_loop.va`.
- Preserve the public module name, positional port order, electrical disciplines, and observable output meanings.
- Do not generate or modify a Spectre testbench.

## Public Verilog-A Interface

Declare module `complete_calibration_loop` with positional ports:

```verilog
module complete_calibration_loop(clk, rst, vin, out, metric, trim_mon, residual_mon);
```

All ports are electrical. `clk` is the loop update clock, `rst` is an
active-high voltage-coded reset, and `vin` is the external error stimulus
around common mode. `trim_mon` exposes the bounded controller trim state,
`residual_mon` exposes the post-correction residual, `out` is the bounded
corrected plant response, and `metric` reports how close the corrected output
is to the target common-mode value.

## Public Parameter Contract

Provide these overrideable public parameters:

- `tr = 100p`: transition time used for smoothed voltage contributions.
- `vth = 0.45 V`: threshold for voltage-coded clock and reset decisions.
- `target = 0.45 V`: common-mode target for the loop.
- `loop_gain = 0.40`: controller gain applied to residual error.
- `plant_alpha = 0.35`: first-order plant update factor.
- `vmin = 0.05 V`, `vmax = 0.85 V`: clamp range for bounded analog states.

## Required Behavior

On reset, initialize the trim state, residual monitor, corrected output, and
metric to their target states. After reset releases, update the loop on rising
clock crossings. Compute the residual from the input error and the current trim
state, drive the trim correction opposite the residual, clamp all bounded
analog states to the public range, and update the corrected plant response
toward the corrected residual. `metric` should be high when `out` is near the
target and should decrease as the output error grows.

## Modeling Constraints

Use voltage contributions only. Use event-updated behavioral state on the clock
edge and `transition(...)` smoothing for output contributions. Do not add
checker logic, hard-code private waveform sample points, add simulator-private
side channels, use current contributions, transistor-level devices, `ddt()`,
`idt()`, or AC/noise-analysis behavior. Companion Verilog-A files referenced by
a testbench are supplied by the harness; the candidate implementation should
contain only `complete_calibration_loop.va`.

## Output Contract

Return exactly one complete Verilog-A file named `complete_calibration_loop.va`.
Do not include explanatory prose outside the source artifact contents.

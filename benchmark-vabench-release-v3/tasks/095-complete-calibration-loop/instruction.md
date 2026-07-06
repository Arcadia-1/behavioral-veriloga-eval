# Complete Calibration Loop

## Task Contract

Implement the requested Verilog-A artifact for `Complete Calibration Loop`.
- Form: `dut`
- Level: `L2`
- Category: `calibration_dem_control`
- Target artifact(s): `complete_calibration_loop.va`

- Base function: closed calibration loop
- Domain: `voltage`

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
validation logic, hard-code specific waveform sample points, add simulator-specific
side channels, use current contributions, transistor-level devices, `ddt()`,
`idt()`, or AC/noise-analysis behavior. Companion Verilog-A files referenced by
a testbench are supplied by the harness; the candidate implementation should
contain only `complete_calibration_loop.va`.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete Verilog-A file named `complete_calibration_loop.va`.
Do not include explanatory prose outside the source artifact contents.

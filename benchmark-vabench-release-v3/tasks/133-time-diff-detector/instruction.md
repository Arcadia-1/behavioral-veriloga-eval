# Time Diff Detector

## Task Contract

Implement a clocked edge time-difference detector that converts input crossing
timing into a bounded voltage.

- Form: `dut`
- Level: `L1`
- Category: mixed-signal timing utility
- Target artifact: `time_diff_detector.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`time_diff_detector.va` must declare:

```verilog
module time_diff_detector(clk, vinp, vinn, vout);
input clk, vinp, vinn;
output vout;
electrical clk, vinp, vinn, vout;
```

## Public Parameter Contract

- `vdd = 0.9`: output clipping magnitude in volts.
- `vth_clk = 0.45`: rising clock-edge threshold in volts.
- `vth_in = 0.45`: rising input-edge threshold in volts.
- `scale = 1e9`: multiplier from seconds to output volts before clipping.
- `td = 0`, `tr = 1p`: output transition delay and rise/fall timing.

## Required Behavior

On each rising threshold crossing of `clk`, publish the previous acquisition
cycle's first `vinp` rising-edge time minus first `vinn` rising-edge time,
multiplied by `scale` and clipped to `[-vdd, +vdd]`.

After publishing on the clock edge, arm a new acquisition cycle. In each cycle,
record only the first rising threshold crossing of `vinp` and only the first
rising threshold crossing of `vinn`. Before a complete prior cycle exists, the
output starts at zero.

## Modeling Constraints

Use `cross`-style event detection for the public thresholds and a
transition-shaped voltage output. Do not measure falling edges, accumulate
multiple crossings per cycle, remove output clipping, or hard-code testbench
edge times.

## Output Contract

Return exactly one source artifact named `time_diff_detector.va`.

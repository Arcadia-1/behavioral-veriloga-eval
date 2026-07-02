# Pipe 2-Lane Edge Align

Implement `pipe_2lane_edge_align.va` as a voltage-domain two-lane alignment
selector for a time-interleaved converter path.

## Public Interface

Use this module signature:

```verilog
module pipe_2lane_edge_align(din1, din2, clk_align, dout);
```

All ports are electrical. `din1` and `din2` are analog lane values,
`clk_align` is the alignment clock, and `dout` is the held aligned output.

## Public Parameter Contract

- `vth` is the clock threshold, default `0.45`.
- The output should use short transition smoothing suitable for sampled analog
  behavioral models.

## Functional Contract

Initialize the held output from `din1`. On each rising crossing of `clk_align`
through `vth`, sample and hold `din1`. On each falling crossing, sample and hold
`din2`. Between clock edges, keep driving the most recently selected lane.

## Modeling Constraints

Use pure voltage-domain event-driven Verilog-A. Do not hard-code stimulus times,
testbench waveforms, simulator-private signals, or checker-only sample points.

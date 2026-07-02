# Pipe15 Data Align

Implement `pipe15_data_align.va` as a voltage-domain latency aligner for a
15-bit pipelined converter readout.

## Public Interface

Use this module signature:

```verilog
module pipe15_data_align(
    samp,
    d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14,
    do0, do1, do2, do3, do4, do5, do6, do7, do8, do9, do10, do11, do12, do13, do14
);
```

All ports are electrical. `samp` is the sampling clock, `d0..d14` are voltage
logic inputs, and `do0..do14` are the aligned voltage logic outputs.

## Public Parameter Contract

- `vth` is the sample-clock and logic threshold, default `0.45`.
- `tt` is the output transition time, default `20p`.

## Functional Contract

On each rising `samp` crossing, capture all input bits and align the output
latency by bit group:

- `do0..do2` publish the current sampled values.
- `do3..do6` publish values delayed by one sample.
- `do7..do10` publish values delayed by two samples.
- `do11..do14` publish values delayed by four samples.

Before a delayed group has enough history, drive that group low. Between sample
edges, hold the most recently published aligned outputs.

## Modeling Constraints

Use pure voltage-domain event-driven Verilog-A. Do not hard-code visible
stimulus timing, private sample points, or checker-only vectors.

# Programmable Stimulus Sequencer

Implement `programmable_stimulus_sequencer.va` in Verilog-A.

## Interface

Declare module `programmable_stimulus_sequencer` with positional ports
`clk, rst, mode, gate, out, metric`. All ports are electrical.

## Public Parameter Contract

- `tr = 80 ps`: output transition smoothing time.

## Functional Contract

This is a voltage-domain stimulus-source DUT, not a Spectre testbench. `clk`,
`rst`, `mode`, and `gate` are voltage-coded control inputs with low level near
0 V, high level near 0.9 V, and a 0.45 V decision threshold.

When reset is high, drive `out` near 0.45 V and `metric` low. Otherwise:

- ramp mode, selected when `mode < 0.30 V`, drives a monotonic ramp segment
  from roughly 0.18 V toward 0.45 V and marks `metric` near 0.20 V;
- chirp mode, selected when `0.30 V <= mode < 0.60 V`, drives a sine segment
  centered near 0.45 V whose instantaneous frequency increases over the
  segment and marks `metric` near 0.50 V;
- burst mode, selected when `mode >= 0.60 V`, drives a gated PRBS-like burst
  between low and high stimulus levels while `gate` is high, returns `out` near
  0.45 V while `gate` is low, and marks `metric` near the burst/idle segment
  status.

The control schedule is supplied by the public/hidden transient benches. The
DUT may use absolute transient time to implement the segment shapes, but should
derive mode and gating decisions from the voltage-coded inputs.

## Modeling Constraints

Return only `programmable_stimulus_sequencer.va`. Do not generate a Spectre
testbench or checker logic. Do not use current contributions, `ddt()`, `idt()`,
transistor-level devices, AC/noise analysis, or simulator-private side
channels.

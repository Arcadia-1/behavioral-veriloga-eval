# TDC Ideal Edge Delta

## Task Contract

Implement an ideal edge-interval timing detector for a TDC-style measurement
primitive.

- Form: `dut`
- Level: `L1`
- Category: measurement/timing support primitive
- Target artifact: `tdc_ideal_edge_delta.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`tdc_ideal_edge_delta.va` must declare:

```verilog
module tdc_ideal_edge_delta(inp, inn, samp, vout);
input inp, inn, samp;
output vout;
electrical inp, inn, samp, vout;
```

## Public Parameter Contract

- `vth = 0.45`: rising-edge threshold in volts for `inp`, `inn`, and `samp`.
- `fullrange = 100p`: normalization interval in seconds.

## Required Behavior

At `initial_step`, clear the input trigger flags and initialize the output state
to zero. On each rising `samp` threshold crossing, clear only the trigger flags
for a new measurement window; keep the previous output until a new input-edge
pair is measured.

Within each measurement window, record the rising threshold crossing time of
`inp` and the rising threshold crossing time of `inn`. After both have occurred,
drive the output state with `(time_inp - time_inn) / fullrange`.

## Modeling Constraints

Use voltage-domain event detection and a transition-shaped voltage output. Do
not count falling edges, clear the output on `samp`, clip the normalized result,
or hard-code testbench edge times.

## Output Contract

Return exactly one source artifact named `tdc_ideal_edge_delta.va`.

# Two Channel Sample Demux

## Task Contract

Implement a two-clock analog sample router that forwards one of two sample
inputs to a shared output.

- Form: `dut`
- Level: `L1`
- Category: sampled-data analog routing
- Target artifact: `two_channel_sample_demux.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`two_channel_sample_demux.va` must declare:

```verilog
module two_channel_sample_demux(samp1, samp2, clks1, clks2, vout);
input samp1, samp2, clks1, clks2;
output vout;
electrical samp1, samp2, clks1, clks2, vout;
```

## Public Parameter Contract

- `vth = 0.45`: rising-edge threshold in volts for both clock inputs.

## Required Behavior

Initialize the output state to `0 V`. On each rising threshold crossing of
`clks1`, update the output state to `V(samp1)`. On each rising threshold
crossing of `clks2`, update the output state to `V(samp2)`. Hold the most
recently selected sample between clock edges.

## Modeling Constraints

Use voltage-domain event updates and a transition-shaped output. Do not average
the two sample inputs, update continuously, use falling edges, or hard-code
testbench waveform values.

## Output Contract

Return exactly one source artifact named `two_channel_sample_demux.va`.

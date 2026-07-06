# Ideal Sample And Hold

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Sampling/Data Converter Support
- Domain: voltage-domain behavioral Verilog-A
- Target artifact: `source_sample_hold.va`
- Required module: `source_sample_hold`

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact.
- Preserve the public module name, port order, parameters, and waveform observable names.
- Model a reusable ideal sample-and-hold primitive.

## Public Verilog-A Interface

`source_sample_hold.va` declares module `source_sample_hold` with positional
ports:

```verilog
module source_sample_hold(vin, vout, vclk);
```

All ports are electrical. `vin` is the analog input, `vclk` is the sampling
clock, and `vout` is the held output.

## Public Parameter Contract

- `vtrans_clk = 0.45 V`: rising-clock threshold.
- `tr = 20p`: transition smoothing time for `vout`.

## Required Behavior

On each rising crossing of `vclk` through `vtrans_clk`, sample the instantaneous
input voltage `V(vin)`. Hold that sampled value between rising clock events and
drive it on `vout` with a smoothed voltage transition. The public observable
waveforms are the input, sampling clock, and held output.

## Modeling Constraints

Use voltage-domain event-driven Verilog-A only. Do not use current
contributions, transistor-level devices, `ddt()`, `idt()`, checker logic, or
testbench-specific timing constants inside the DUT.

## Output Contract

Return exactly one complete Verilog-A source artifact named
`source_sample_hold.va`. Do not include explanatory prose outside the source
artifact contents.

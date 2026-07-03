# Four Channel Edge Sampler

## Task Contract

Implement a four-channel analog sample-and-hold bank triggered by a shared clock
edge.

- Form: `dut`
- Level: `L1`
- Category: sampled-data analog routing
- Target artifact: `four_channel_edge_sampler.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`four_channel_edge_sampler.va` must declare:

```verilog
module four_channel_edge_sampler(clk, vin0, vin1, vin2, vin3,
                                 vout0, vout1, vout2, vout3);
input clk, vin0, vin1, vin2, vin3;
output vout0, vout1, vout2, vout3;
electrical clk, vin0, vin1, vin2, vin3, vout0, vout1, vout2, vout3;
```

## Public Parameter Contract

- `direction = 1`: `cross` direction for the sampling clock edge.
- `vdd = 1.2`: clock high level; sampling threshold is `vdd/2`.
- `td = 0`, `tr = 50p`, `tf = 50p`: output transition delay, rise time, and
  fall time.

## Required Behavior

Initialize all four held output values to `0 V`. On each selected clock
threshold crossing, sample `vin0` through `vin3` simultaneously and hold those
values on `vout0` through `vout3` until the next selected edge.

## Modeling Constraints

Use voltage-domain sample-and-hold state and transition-shaped outputs. Do not
track the inputs continuously, sample only one channel, change channel order, or
hard-code testbench edge times.

## Output Contract

Return exactly one source artifact named `four_channel_edge_sampler.va`.

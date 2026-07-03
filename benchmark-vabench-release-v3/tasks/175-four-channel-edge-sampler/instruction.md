# Four Channel Edge Sampler

## Task Contract
Implement the Verilog-A DUT `four_channel_edge_sampler.va` for simultaneous sampling of four analog channels on a configurable clock edge.

## Form-Specific Requirements
This is a single-DUT sampled analog memory task. The four outputs should update only when the clock crosses the public threshold in the configured direction.

## Public Verilog-A Interface
Provide `module four_channel_edge_sampler(clk, vin0, vin1, vin2, vin3, vout0, vout1, vout2, vout3);` with electrical input `clk`, electrical inputs `vin0` through `vin3`, and electrical outputs `vout0` through `vout3`.

## Public Parameter Contract
Expose `direction = 1`, `vdd = 1.2`, `tr = 50p`, `tf = 50p`, and `td = 0`. Testbenches may override these parameters.

## Required Behavior
Initialize all sampled outputs to zero. On each `cross(V(clk) - vdd/2, direction)`, simultaneously sample `vin0` through `vin3` into the corresponding outputs. Drive each output with `transition(sample, td, tr, tf)`.

## Modeling Constraints
Use one shared clock event for all four channels and preserve channel order. Do not swap channels, update only one channel, or continuously track the inputs between clock edges.

## Output Contract
Submit only the completed Verilog-A module in `four_channel_edge_sampler.va`.

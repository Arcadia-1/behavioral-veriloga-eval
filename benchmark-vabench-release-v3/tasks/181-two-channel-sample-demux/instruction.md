# Two Channel Sample Demux

## Task Contract
Implement the Verilog-A DUT `two_channel_sample_demux.va` for two clocked analog sample sources driving one output.

## Form-Specific Requirements
This is a single-DUT sampled routing task. The output is event-updated by either clock input and should hold its previous value between events.

## Public Verilog-A Interface
Provide `module two_channel_sample_demux(samp1, samp2, clks1, clks2, vout);` with electrical inputs `samp1`, `samp2`, `clks1`, `clks2` and electrical output `vout`.

## Public Parameter Contract
Expose `parameter real vth = 0.45;`. Testbenches may override this parameter.

## Required Behavior
Initialize `vout` to zero. On a rising `clks1` crossing of `vth`, sample `samp1` into the output state. On a rising `clks2` crossing of `vth`, sample `samp2` into the output state. Drive `vout` through a `10p` rise/fall transition.

## Modeling Constraints
Use event-driven analog state. Do not swap the two sample sources, ignore the second clock, or continuously average/track the inputs.

## Output Contract
Submit only the completed Verilog-A module in `two_channel_sample_demux.va`.

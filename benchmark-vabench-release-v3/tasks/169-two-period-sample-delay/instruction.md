# Two Period Sample Delay

## Task Contract
Implement the Verilog-A DUT `two_period_sample_delay.va` for an edge-updated sampled-data delay element.

## Form-Specific Requirements
This is a single-DUT sampled analog memory task. The DUT should react to update edges and input values, not to fixed times from the public testbench.

## Public Verilog-A Interface
Provide `module two_period_sample_delay(update, ain, aout);` with electrical inputs `update`, `ain` and electrical output `aout`.

## Public Parameter Contract
Expose `vth = 0.5`, `tr = 50p`, and `init = 0.0`. Testbenches may override these real parameters.

## Required Behavior
Initialize the stored sample and output to `init`. On each rising `update` crossing of `vth`, drive the output from the sample stored before the current edge, then update the stored sample from `ain`. Drive `aout` through a transition using `tr` for rise and fall time.

## Modeling Constraints
Use event-driven analog state. Do not pass `ain` directly to the output, skip initialization, or use the wrong update edge.

## Output Contract
Submit only the completed Verilog-A module in `two_period_sample_delay.va`.

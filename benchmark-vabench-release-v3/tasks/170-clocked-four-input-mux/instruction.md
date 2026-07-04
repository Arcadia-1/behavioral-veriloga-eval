# Clocked Four Input Mux

## Task Contract
Implement the Verilog-A DUT `clocked_four_input_mux.va` for a falling-edge sampled 4:1 analog mux.

## Form-Specific Requirements
This is a single-DUT sampled routing task. Selection is latched on clock events; it should not continuously track select changes between clock edges.

## Public Verilog-A Interface
Provide `module clocked_four_input_mux(dsel0, dsel1, din0, din1, din2, din3, clks, dout);` with electrical inputs `dsel0`, `dsel1`, `din0` through `din3`, `clks` and electrical output `dout`.

## Public Parameter Contract
Expose `vth = 0.45` and `tr = 20p`. Testbenches may override these real parameters.

## Required Behavior
Initialize the registered output from `din0`. On each falling `clks` crossing of `vth`, interpret `dsel0` as the least-significant select bit and `dsel1` as the most-significant select bit, then sample one of `din0` through `din3`. Drive `dout` through a transition with a fixed `1p` delay and rise/fall time `tr`.

## Modeling Constraints
Use clocked analog state and thresholded select bits. Do not latch on the rising clock edge, swap select-bit order, or ignore `dsel1`.

## Output Contract
Submit only the completed Verilog-A module in `clocked_four_input_mux.va`.

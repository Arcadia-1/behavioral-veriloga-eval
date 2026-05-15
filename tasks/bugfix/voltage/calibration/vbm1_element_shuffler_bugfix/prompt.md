# Task: vbm1_element_shuffler_bugfix

Repair the provided Verilog-A element shuffler. The DUT has one clock input
`clk`, an active-low reset input `rst_n`, and four voltage-domain one-hot
outputs `out0`, `out1`, `out2`, and `out3`.

After reset is released, each rising edge of `clk` advances the internal state
through the shuffle order `0 -> 2 -> 1 -> 3 -> 0`. The public output sequence
sampled after the first six rising edges must therefore be:

`out1, out2, out3, out0, out1, out2`.

Keep outputs voltage-domain only and drive them with `transition`. Do not use
current contributions.

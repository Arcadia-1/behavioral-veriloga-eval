# Task: vbm1_rotating_element_selector_bugfix

Repair the provided Verilog-A rotating element selector. The DUT has one clock
input `clk`, an active-low reset input `rst_n`, and four voltage-domain one-hot
outputs `sel0`, `sel1`, `sel2`, and `sel3`.

After reset is released, each rising edge of `clk` increments the selector and
wraps after state 3. The public output sequence sampled after the first six
rising edges must be:

`sel1, sel2, sel3, sel0, sel1, sel2`.

Keep outputs voltage-domain only and drive them with `transition`. Do not use
current contributions.

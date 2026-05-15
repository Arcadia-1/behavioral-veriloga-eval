# Task: vbm1_debounce_latch_bugfix

Repair the provided Verilog-A debounce latch. The DUT has voltage-domain input
`sig`, active-high reset release input `rst_n`, and voltage-domain output
`out`.

When reset is asserted low, clear the latched state. After reset is released,
only latch `out` high if `sig` rises above threshold and stays high for the
configured debounce interval. Short pulses before the interval expires must not
set the latch.

Keep the model purely voltage-domain and drive `out` with `transition`. Do not
use current contributions.

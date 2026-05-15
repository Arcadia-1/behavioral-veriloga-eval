# Task: vbm1_edge_detector_bugfix

The provided voltage-domain edge detector has an edge-polarity bug: it produces
the output pulse on the falling edge of `sig` instead of the rising edge. Fix
the design so it emits one bounded-width pulse after each rising `sig` crossing
while reset is released.

The fixed module must be named `edge_detector` and use electrical ports `sig`,
`rst_n`, and `pulse`. When `rst_n` is low, the pulse output must be low and the
internal one-shot state must be cleared. When reset is released, each rising
edge of `sig` should arm a pulse with the configured width and then clear it.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.

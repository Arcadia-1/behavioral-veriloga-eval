# Task: vbm1_first_order_lowpass_dut

Write a pure voltage-domain Verilog-A module for a timer-discretized first-order lowpass.

The DUT module is `first_order_lowpass` with ports `vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Use a 500 ps timer update with state `y += 0.025 * (V(vin) - y)`.
- Drive `vout` from the internal state with `transition()`.
- The response must be monotone and visibly slower than an instantaneous copy.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `first_order_lowpass.va`.

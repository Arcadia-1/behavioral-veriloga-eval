# Task: vbm1_first_order_lowpass_tb

Write a Spectre testbench for a timer-discretized first-order lowpass DUT.

The DUT module is `first_order_lowpass` with ports `vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `first_order_lowpass.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Use a 500 ps timer update with state `y += 0.025 * (V(vin) - y)`.
- Drive `vout` from the internal state with `transition()`.
- The response must be monotone and visibly slower than an instantaneous copy.

Stimulus and observability requirements:
- Apply a 0 to high step on `vin` and run long enough for the lowpass output to settle.
- Save `vin` and `vout` for fixed-time response checks.

Return exactly one Spectre testbench file named `tb_first_order_lowpass_ref.scs`.

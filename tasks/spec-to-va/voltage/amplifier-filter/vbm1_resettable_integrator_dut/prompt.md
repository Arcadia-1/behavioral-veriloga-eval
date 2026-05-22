# Task: vbm1_resettable_integrator_dut

Write a pure voltage-domain Verilog-A module for a resettable timer integrator.

The DUT module is `resettable_integrator` with ports `vin, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Use a 1 ns timer update to integrate `vin` into an internal accumulator.
- High `rst` clears the accumulator to 0 V.
- Clamp the accumulator between 0 V and 0.85 V and drive `vout` with `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `resettable_integrator.va`.

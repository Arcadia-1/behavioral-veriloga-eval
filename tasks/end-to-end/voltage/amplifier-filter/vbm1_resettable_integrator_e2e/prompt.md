# Task: vbm1_resettable_integrator_e2e

Write both the Verilog-A DUT and Spectre testbench for a resettable timer integrator.

The DUT module is `resettable_integrator` with ports `vin, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Use a 1 ns timer update to integrate `vin` into an internal accumulator.
- High `rst` clears the accumulator to 0 V.
- Clamp the accumulator between 0 V and 0.85 V and drive `vout` with `transition()`.

Required testbench behavior:
- Drive a positive input, reset pulse, and post-reset positive input interval.
- Save `vin`, `rst`, and `vout` across pre-reset integration, reset clearing, and restart windows.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `resettable_integrator.va` and `tb_resettable_integrator_ref.scs`.

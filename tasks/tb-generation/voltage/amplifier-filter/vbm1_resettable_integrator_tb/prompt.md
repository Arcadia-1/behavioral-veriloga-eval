# Task: vbm1_resettable_integrator_tb

Write a Spectre testbench for a resettable timer integrator DUT.

The DUT module is `resettable_integrator` with ports `vin, rst, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `resettable_integrator.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Use a 1 ns timer update to integrate `vin` into an internal accumulator.
- High `rst` clears the accumulator to 0 V.
- Clamp the accumulator between 0 V and 0.85 V and drive `vout` with `transition()`.

Stimulus and observability requirements:
- Drive a positive input, reset pulse, and post-reset positive input interval.
- Save `vin`, `rst`, and `vout` across pre-reset integration, reset clearing, and restart windows.

Return exactly one Spectre testbench file named `tb_resettable_integrator_ref.scs`.

# Task: vbm1_slew_rate_limiter_tb

Write a Spectre testbench for a discrete slew-rate limiter DUT.

The DUT module is `slew_rate_limiter` with ports `vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `slew_rate_limiter.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Use a 1 ns timer update and move the internal output toward `vin` by at most 0.015 V per update.
- Limit both rising and falling changes and drive `vout` with `transition()`.

Stimulus and observability requirements:
- Apply a large upward step, hold, then a downward step.
- Save `vin` and `vout` to verify limited rising and falling slopes and eventual settling.

Return exactly one Spectre testbench file named `tb_slew_rate_limiter_ref.scs`.

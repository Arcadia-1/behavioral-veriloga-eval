# Task: vbm1_thermometer_decoder_guarded_tb

Write a Spectre testbench for a guarded thermometer decoder DUT.

The DUT module is `thermometer_decoder_guarded` with ports `b0, b1, en, th0, th1, th2, th3`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `thermometer_decoder_guarded.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Decode a 2-bit binary input into cumulative thermometer outputs while `en` is high.
- With `en` low, force all thermometer outputs low.
- For codes 1, 2, and 3, assert `th0`, then `th0:th1`, then `th0:th2`; `th3` remains guarded low for this 2-bit input space.

Stimulus and observability requirements:
- Exercise enable-low, code 1, code 2, and code 3 windows.
- Save inputs and all thermometer outputs.

Return exactly one Spectre testbench file named `tb_thermometer_decoder_guarded_ref.scs`.

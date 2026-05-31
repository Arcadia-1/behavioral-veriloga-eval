# Task: vbm1_thermometer_decoder_guarded_e2e

Write both the Verilog-A DUT and Spectre testbench for a guarded thermometer decoder.

The DUT module is `thermometer_decoder_guarded` with ports `b0, b1, en, th0, th1, th2, th3`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Decode a 2-bit binary input into cumulative thermometer outputs while `en` is high.
- With `en` low, force all thermometer outputs low.
- For codes 1, 2, and 3, assert `th0`, then `th0:th1`, then `th0:th2`; `th3` remains guarded low for this 2-bit input space.

Required testbench behavior:
- Exercise enable-low, code 1, code 2, and code 3 windows.
- Save inputs and all thermometer outputs.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `thermometer_decoder_guarded.va` and `tb_thermometer_decoder_guarded_ref.scs`.

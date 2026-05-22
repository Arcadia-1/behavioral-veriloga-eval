# Task: vbm1_precision_rectifier_e2e

Write both the Verilog-A DUT and Spectre testbench for a ideal precision rectifier.

The DUT module is `precision_rectifier` with ports `vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Drive `vout` to `vin` when `vin` is positive and to 0 V when `vin` is negative.
- Use only voltage-domain contributions and smooth the output with `transition()`.

Required testbench behavior:
- Apply negative, near-zero, and positive input intervals.
- Save `vin` and `vout` for rectification checks.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `precision_rectifier.va` and `tb_precision_rectifier_ref.scs`.

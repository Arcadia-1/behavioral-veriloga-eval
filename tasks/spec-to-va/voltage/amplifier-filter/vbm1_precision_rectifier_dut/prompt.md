# Task: vbm1_precision_rectifier_dut

Write a pure voltage-domain Verilog-A module for a ideal precision rectifier.

The DUT module is `precision_rectifier` with ports `vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Drive `vout` to `vin` when `vin` is positive and to 0 V when `vin` is negative.
- Use only voltage-domain contributions and smooth the output with `transition()`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `precision_rectifier.va`.

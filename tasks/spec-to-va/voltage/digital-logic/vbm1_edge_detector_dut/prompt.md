# Task: vbm1_edge_detector_dut

Write a pure voltage-domain Verilog-A module named `edge_detector`.

The module has electrical ports `sig`, `rst_n`, and `pulse`. `rst_n` is active
low. After reset is released, each rising crossing of `sig` should generate a
short high pulse on `pulse`; falling crossings must not generate a pulse. Drive
outputs with `transition` and use voltage contributions only.

Return exactly one complete Verilog-A file named `edge_detector.va`.

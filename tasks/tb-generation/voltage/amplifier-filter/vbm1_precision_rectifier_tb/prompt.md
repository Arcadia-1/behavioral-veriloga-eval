# Task: vbm1_precision_rectifier_tb

Write a Spectre testbench for a ideal precision rectifier DUT.

The DUT module is `precision_rectifier` with ports `vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `precision_rectifier.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Drive `vout` to `vin` when `vin` is positive and to 0 V when `vin` is negative.
- Use only voltage-domain contributions and smooth the output with `transition()`.

Stimulus and observability requirements:
- Apply negative, near-zero, and positive input intervals.
- Save `vin` and `vout` for rectification checks.

Return exactly one Spectre testbench file named `tb_precision_rectifier_ref.scs`.

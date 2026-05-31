# Task: vbm1_voltage_clamp_e2e

Write both the Verilog-A DUT and Spectre testbench for a voltage clamp.

The DUT module is `voltage_clamp` with ports `raw_level, vdd, vss, clamped_level`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Clamp `raw_level` to the public range 0.18 V to 0.72 V.
- Drive `clamped_level` through `transition()` using voltage-domain contributions only.

Required testbench behavior:
- Drive `raw_level` below range, inside range, and above range.
- Save `raw_level`, supplies, and `clamped_level`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `dut.va` and `tb_ref.scs`.

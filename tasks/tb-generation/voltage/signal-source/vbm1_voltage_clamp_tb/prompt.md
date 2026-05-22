# Task: vbm1_voltage_clamp_tb

Write a Spectre testbench for a voltage clamp DUT.

The DUT module is `voltage_clamp` with ports `raw_level, vdd, vss, clamped_level`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `dut.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Clamp `raw_level` to the public range 0.18 V to 0.72 V.
- Drive `clamped_level` through `transition()` using voltage-domain contributions only.

Stimulus and observability requirements:
- Drive `raw_level` below range, inside range, and above range.
- Save `raw_level`, supplies, and `clamped_level`.

Return exactly one Spectre testbench file named `tb_ref.scs`.

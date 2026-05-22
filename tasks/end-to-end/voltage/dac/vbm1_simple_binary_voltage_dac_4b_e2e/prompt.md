# Task: vbm1_simple_binary_voltage_dac_4b_e2e

Write both the Verilog-A DUT and Spectre testbench for a simple 4-bit binary-coded DAC.

The DUT module is `simple_binary_voltage_dac_4b` with ports `code_0, code_1, code_2, code_3, vref, vss, aout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Implement the simple mathematical 4-bit binary-coded DAC described by the input code and references.
- Interpret `code_0..code_3` as a binary code with weights 1, 2, 4, and 8.
- Drive `aout` linearly between `vss` and `vref` using code/15 and smooth with `transition()`; no unit-element or segmented DAC structure is required.

Required testbench behavior:
- Apply multiple binary codes spanning low, middle, and full-scale values.
- Save all code bits and `aout`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Review note: This is a behavioral binary-weighted transfer model, not a unit-element or segmented DAC implementation.

Return exactly two files: `simple_binary_voltage_dac_4b.va` and `tb_simple_binary_voltage_dac_4b_ref.scs`.

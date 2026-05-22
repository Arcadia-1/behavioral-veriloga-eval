# Task: vbm1_simple_binary_voltage_dac_4b_tb

Write a Spectre testbench for a simple 4-bit binary-coded DAC DUT.

The DUT module is `simple_binary_voltage_dac_4b` with ports `code_0, code_1, code_2, code_3, vref, vss, aout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `simple_binary_voltage_dac_4b.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Implement the simple mathematical 4-bit binary-coded DAC described by the input code and references.
- Interpret `code_0..code_3` as a binary code with weights 1, 2, 4, and 8.
- Drive `aout` linearly between `vss` and `vref` using code/15 and smooth with `transition()`; no unit-element or segmented DAC structure is required.

Stimulus and observability requirements:
- Apply multiple binary codes spanning low, middle, and full-scale values.
- Save all code bits and `aout`.

Review note: This is a behavioral binary-weighted transfer model, not a unit-element or segmented DAC implementation.

Return exactly one Spectre testbench file named `tb_simple_binary_voltage_dac_4b_ref.scs`.

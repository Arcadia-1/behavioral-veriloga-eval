# Task: vbm1_resettable_counter_divider_e2e

Write both the Verilog-A DUT and Spectre testbench for a resettable programmable clock divider.

The DUT module is `clk_divider_ref` with ports `clk_in, rst_n, div_code_0, div_code_1, div_code_2, div_code_3, div_code_4, div_code_5, div_code_6, div_code_7, clk_out, lock`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Decode an 8-bit voltage-domain ratio code into an integer divide ratio, with code 0 treated as ratio 1.
- Use active-low reset to clear the counter, output state, and lock state.
- For ratio greater than 1, divide the input clock with floor/ceil high and low segment lengths; assert `lock` after the first complete output period.

Required testbench behavior:
- Drive `div_code` to ratio 5, release reset near 2 ns, and clock with a 1 ns input period.
- Run to 80 ns with a small maxstep and save input clock, output clock, lock, reset, and all ratio bits.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Review caveat: The staged evidence also preserves an auxiliary legacy `clk_divider.va`; the public task contract targets `clk_divider_ref`.

Return exactly two files: `clk_divider_ref.va` and `tb_clk_divider_ref.scs`.

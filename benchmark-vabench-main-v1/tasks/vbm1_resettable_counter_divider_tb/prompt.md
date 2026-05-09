Given a voltage-domain programmable divider DUT, generate only a Spectre testbench.
Do not generate Verilog-A modules.

Provided DUT:
- Include file: `clk_divider_ref.va`
- Module name: `clk_divider_ref`
- Positional port order: `(clk_in rst_n div_code_0 div_code_1 div_code_2 div_code_3 div_code_4 div_code_5 div_code_6 div_code_7 clk_out lock)`

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Include `clk_divider_ref.va` using `ahdl_include`.
- Drive `clk_in` with a 1 ns period clock.
- Release active-low `rst_n` after startup and keep it high.
- Set ratio code 5.
- Save plain scalar names: `clk_in`, `rst_n`, `clk_out`, `lock`, and all `div_code_*` bits.
- Run exactly `tran tran stop=80n maxstep=50p`.

Return exactly one fenced `spectre` code block.

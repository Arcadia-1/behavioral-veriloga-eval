Write a programmable resettable clock divider DUT and a minimal Spectre testbench.

Required DUT module: `clk_divider_ref`.
Ports, all `electrical`, exactly as named and ordered:
`clk_in`, `rst_n`, `div_code_0` ... `div_code_7`, `clk_out`, `lock`.

DUT behavior:
- Interpret the eight `div_code_*` inputs as an unsigned division ratio, clamped to at least 1.
- Synchronous active-low reset clears internal count, output state, and `lock`.
- Generate a divided `clk_out` whose edge intervals match the public ratio.
- Assert `lock` after the first complete output period.
- Use voltage-domain contributions and `transition(...)`.

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Drive `clk_in` with a 1 ns period clock.
- Release `rst_n` after startup and keep it high.
- Set the public ratio to 5 using `div_code_0=1` and `div_code_2=1`.
- Save plain scalar names: `clk_in`, `rst_n`, `clk_out`, `lock`, and all `div_code_*` bits.
- Run exactly `tran tran stop=80n maxstep=50p`.

Return two fenced code blocks: one `verilog-a` block and one `spectre` block.

Write a pure Verilog-A offset comparator DUT and a minimal Spectre testbench.

Required DUT module: `cmp_offset_ref`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `CLK`, `VINP`, `VINN`, `OUT_P`.

DUT behavior:
- On each rising edge of `CLK`, compare `VINP - VINN` against the public real parameter `vos`.
- Drive `OUT_P` high only when `VINP - VINN > vos`; otherwise drive it low.
- Use voltage-domain contributions and `transition(...)`.

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Provide `VDD=0.9 V` and `VSS=0 V`.
- Drive `CLK` with repeated rising edges.
- Drive `VINP` and `VINN` so both below-offset and above-offset decisions occur.
- Instantiate the DUT by positional ports.
- Save plain scalar names: `CLK`, `VINP`, `VINN`, `OUT_P`.
- Run exactly `tran tran stop=28n maxstep=20p`.
- Include `cmp_offset_ref.va` using `ahdl_include`.

Return two fenced code blocks: one `verilog-a` block for `cmp_offset_ref.va` and one `spectre` block for the testbench.

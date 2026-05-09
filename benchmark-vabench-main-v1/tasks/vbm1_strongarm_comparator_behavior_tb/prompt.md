Given a voltage-domain StrongARM-style comparator DUT, generate a minimal Spectre-format testbench.
Do not generate Verilog-A modules.

Provided DUT:
- Include file: `cmp_strongarm.va`
- Module name: `cmp_strongarm`
- Positional port order: `(CLK VINN VINP DCMPN DCMPP LP LM VSS VDD)`

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Provide a 0.9 V supply and 0 V reference.
- Generate a clock near 1 GHz.
- Drive `vinp` and `vinn` so the input polarity changes during the run.
- Instantiate the DUT by positional ports.
- Save plain scalar names: `clk`, `vinp`, `vinn`, `out_p`, `out_n`.
- Run exactly `tran tran stop=4n maxstep=5p`.
- Include `cmp_strongarm.va` using `ahdl_include`.

Return exactly one fenced `spectre` code block.

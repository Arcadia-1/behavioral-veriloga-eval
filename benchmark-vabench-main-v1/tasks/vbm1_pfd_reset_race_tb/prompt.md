Given a pure voltage-domain PFD DUT, generate a minimal Spectre-format testbench.
Do not generate Verilog-A modules.

Provided DUT:
- Include file: `pfd_updn.va`
- Module name: `pfd_updn`
- Positional port order: `(VDD VSS REF DIV UP DN)`

Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Provide 0.9 V `vdd` and 0 V `vss`.
- Drive `ref` and `div` with rising edges whose lead/lag relationship swaps during the transient.
- Instantiate the DUT by positional ports.
- Save plain scalar names: `ref`, `div`, `up`, `dn`.
- Run exactly `tran tran stop=300n maxstep=10p errpreset=conservative`.
- Include `pfd_updn.va` using `ahdl_include`.

Return exactly one fenced `spectre` code block.

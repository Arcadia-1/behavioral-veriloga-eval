Given a voltage-domain 4-bit SAR logic DUT, generate only a Spectre testbench.
Do not generate Verilog-A modules.

Provided DUT:
- Include file: `sar_logic_4b.va`
- Module name: `sar_logic_4b`
- Positional port order: `(VDD VSS CLKS DCOMP DP_DAC_3 DP_DAC_2 DP_DAC_1 DP_DAC_0 RDY)`

Required module: `sar_logic_4b`.
Ports, all `electrical`, exactly as named and ordered:
`VDD`, `VSS`, `CLKS`, `DCOMP`, `DP_DAC_3`, `DP_DAC_2`, `DP_DAC_1`, `DP_DAC_0`, `RDY`.

Behavior:
- Implement a 4-bit SAR control sequence driven by rising edges of `CLKS`.
- Start each conversion by asserting the MSB trial bit.
- On each bit phase, keep or clear the current trial bit from `DCOMP`, then assert the next lower trial bit.
- After four bit decisions, assert `RDY` for one cycle and then start a new conversion.
- Drive all outputs with voltage-domain `transition(...)`.

Public evaluation contract:
- The fixed harness runs `tran tran stop=1.2u maxstep=2n`.
- Public waveform columns include `rdy`, `dp_dac_3`, `dp_dac_2`, `dp_dac_1`, and `dp_dac_0`.


Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Include `sar_logic_4b.va` using `ahdl_include`.
- Provide 0.9 V `VDD` and 0 V `VSS`.
- Drive `CLKS` with a 50 ns period clock.
- Drive `DCOMP` with a repeating waveform so both keep and reject decisions occur.
- Save plain scalar names: `rdy`, `dp_dac_3`, `dp_dac_2`, `dp_dac_1`, and `dp_dac_0`.
- Run exactly `tran tran stop=1.2u maxstep=2n`.

Return exactly one fenced `spectre` code block.

# Weighted SAR ADC DAC Loop

## Task Contract
Build a composed L2 data-converter flow containing a sample/hold, an 8-bit SAR ADC, a weighted reconstruction DAC, and the Spectre transient deck that connects them. The returned artifacts are judged together for conversion sequencing, monitor consistency, and DAC reconstruction behavior.

## Public Verilog-A Interface
Return these public modules and deck:

- `dac_weighted_8b(DIN7, DIN6, DIN5, DIN4, DIN3, DIN2, DIN1, DIN0, VOUT)`, with `DIN7` as MSB and `DIN0` as LSB.
- `sar_adc_weighted_8b(VIN, CLKS, RST_N, DOUT, BIT_INDEX, TRIAL_CODE_MON, TRIAL_VDAC, CMP_DECISION, CONV_DONE, VIN_SAMPLE)`, with `DOUT[7]` as MSB and `DOUT[0]` as LSB.
- `sh_ideal(vin, clk, vdd, vss, rst_n, vout)`.
- `tb_sar_adc_dac_weighted_8b_ref.scs` connecting the flow.

## Public Parameter Contract
The testbench defines the public verification scenario: `vdd=0.9`, a tens-of-MHz sampling clock, active-low reset, and a full-swing sine input. The DUT modules may expose `vdd`, `vth`, and transition parameters where appropriate. The DAC uses binary-weighted 8-bit reconstruction with all-ones code at full scale.

## Required Behavior
The sample/hold captures the analog input after reset. The SAR converter should expose an MSB-to-LSB trial sequence on clock edges, with `trial_code_mon`, `trial_vdac`, `cmp_decision`, `conv_done`, and `vin_sample` behaving as public monitors of the conversion state. Completed conversions should cover a broad input range. The DAC output should reconstruct the final 8-bit code in the `0 V` to `vdd` range and remain consistent with the SAR output bits.

## Modeling Constraints
Use pure voltage-domain, event-driven Verilog-A for the modules and a portable Spectre deck using literal `ahdl_include` lines and instance-first/module-last AHDL syntax. Do not use transistor devices, current contributions, `ddt()`, `idt()`, private checker hooks, generated waveform files, or simulator side channels. Testbench numerical values are public verification settings, not hidden DUT constants unless exposed through parameters or ports.

## Output Contract
Return exactly `dac_weighted_8b.va`, `sar_adc_weighted_8b.va`, `sh_ideal.va`, and `tb_sar_adc_dac_weighted_8b_ref.scs`.

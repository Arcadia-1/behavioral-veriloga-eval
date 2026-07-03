# Weighted SAR ADC DAC Loop

Build a voltage-domain sample/hold, 8-bit SAR conversion, weighted DAC
reconstruction loop, and Spectre testbench. This is an L2 flow benchmark: the
Verilog-A blocks and the testbench are judged together for conversion-sequence
and reconstruction consistency.

## Output Contract

Return exactly these artifacts:

- `dac_weighted_8b.va`
- `sar_adc_weighted_8b.va`
- `sh_ideal.va`
- `tb_sar_adc_dac_weighted_8b_ref.scs`

## Public Interfaces

- `dac_weighted_8b(DIN7, DIN6, DIN5, DIN4, DIN3, DIN2, DIN1, DIN0, VOUT)`,
  with `DIN7` as MSB and `DIN0` as LSB.
- `sar_adc_weighted_8b(VIN, CLKS, RST_N, DOUT, BIT_INDEX, TRIAL_CODE_MON,
  TRIAL_VDAC, CMP_DECISION, CONV_DONE, VIN_SAMPLE)`, with `DOUT[7]` as MSB
  and `DOUT[0]` as LSB.
- `sh_ideal(vin, clk, vdd, vss, rst_n, vout)`.

## Public Testbench Contract

The exact numerical values in this section are the public verification scenario
for the returned Spectre deck, not values that should be hard-coded into the
DUT internals unless they are also exposed as DUT parameters or ports.

The testbench must include the three Verilog-A files with literal
`ahdl_include` lines, use instance-first/module-last AHDL syntax, define
`parameters vdd=0.9 fin=200e3`, drive `clks` as a 50 MHz clock, use active-low
reset `rst_n`, drive `vin` with a full-swing sine, run
`tran tran stop=9u maxstep=5n`, and save `vin`, `vin_sh`, `clks`, `rst_n`,
`vout`, `dout_7` through `dout_0`, `bit_index`, `trial_code_mon`,
`trial_vdac`, `cmp_decision`, `conv_done`, and `vin_sample`.

## Functional Contract

The sample/hold captures the input after reset. The SAR exposes an MSB-to-LSB
trial sequence over clock edges. `trial_code_mon`, `trial_vdac`,
`cmp_decision`, and `vin_sample` must stay mutually consistent as public
monitors of the conversion state. Completed conversions should cover a broad
input range, and the final code should reconstruct through the weighted DAC
into the declared output range.

Use pure voltage-domain event-driven Verilog-A. Do not use transistor devices,
current contributions, `ddt()`, or `idt()`.

# Agent-Visible Spec: vbr1_l2_weighted_sar_adc_dac_loop:e2e

One-shot L2 composed-flow task: implement a voltage-domain sample/hold -> SAR
conversion -> weighted DAC reconstruction flow.

## Required Output

- `dac_weighted_8b.va`
- `sar_adc_weighted_8b.va`
- `sh_ideal.va`
- `tb_sar_adc_dac_weighted_8b_ref.scs`

## Public Interfaces

- `dac_weighted_8b(DIN7, DIN6, DIN5, DIN4, DIN3, DIN2, DIN1, DIN0, VOUT)`;
  `DIN7` is the MSB, `DIN0` is the LSB, and weighted DAC `vout` should stay in
  the `0 V` to `0.9 V` range.
- `sar_adc_weighted_8b(VIN, CLKS, RST_N, DOUT, BIT_INDEX, TRIAL_CODE_MON,
  TRIAL_VDAC, CMP_DECISION, CONV_DONE, VIN_SAMPLE)`. Declare `DOUT` as an
  8-bit electrical vector mapped to scalar `dout_7 ... dout_0`.
- `sh_ideal(vin, clk, vdd, vss, rst_n, vout)`.

## Public Testbench Contract

The Spectre testbench must:

- include `sar_adc_weighted_8b.va`, `dac_weighted_8b.va`, and `sh_ideal.va`
  using literal `ahdl_include` lines;
- use instance-first/module-last AHDL syntax;
- use `parameters vdd=0.9 fin=100e3`;
- drive `clks` as a 50 MHz clock, reset with active-low `rst_n`, and drive
  `vin` with a full-swing sine;
- run `tran tran stop=20u maxstep=5n`;
- save `vin`, `vin_sh`, `clks`, `rst_n`, `vout`, `dout_7`, `dout_6`,
  `dout_5`, `dout_4`, `dout_3`, `dout_2`, `dout_1`, `dout_0`, `bit_index`,
  `trial_code_mon`, `trial_vdac`, `cmp_decision`, `conv_done`, and
  `vin_sample`.

## Functional Contract

- `sh_ideal` samples `vin` after reset and holds `vin_sh`; `vin_sample` should
  match the sampled input used by the converter.
- The SAR consumes the held value, exposes an MSB-to-LSB trial sequence over
  multiple clock edges, and exercises all eight trial positions through
  `bit_index`.
- `trial_code_mon`, `trial_vdac`, `cmp_decision`, and `vin_sample` should be
  mutually consistent except near decision boundaries.
- Completed conversions over the 20u full-swing sine should cover a broad
  range, include codes near both rails, and remain monotonic with sampled input
  within normal quantization tolerance.
- The final `dout_7 ... dout_0` code should reconstruct through weighted DAC
  `vout`; the public relation is `vin_sh`/`vin_sample` -> trial sequence ->
  final code -> `vout`.

## Modeling Constraints

Use pure voltage-domain, event-driven Verilog-A. Drive outputs with voltage
contributions. Do not use transistor-level devices, current-domain loads,
AC/noise analysis, current contributions, `ddt()`, or `idt()`.

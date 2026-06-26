# Gain Extraction Flow

One-shot L2 support flow: build a voltage-domain dithered differential input
path, fixed-gain differential output path, and Spectre transient testbench. This
is a support flow and should be reported separately from core analog/mixed-signal
circuit-function score claims.

## Required Output

- `dither_adder.va`
- `gain_amp_fixed.va`
- `lfsr.va`
- `tb_gain_extraction_ref.scs`
- `vin_src.va`

Do not return `gain_estimator.va` or waveform files.

## Public Interfaces

- `vin_src(CLK, RST_N, VOUT_P, VOUT_N)`
- `lfsr(DPN, VDD, VSS, CLK, EN, RSTB)`
- `dither_adder(VRES_P, VRES_N, DPN, VOUT_P, VOUT_N)`
- `gain_amp_fixed(VIN_P, VIN_N, VOUT_P, VOUT_N)`

All ports are scalar voltage-domain electrical nodes.

## Public Testbench Contract

The Spectre testbench must:

- include `vin_src.va`, `lfsr.va`, `dither_adder.va`, and `gain_amp_fixed.va`
  with literal `ahdl_include` lines;
- use instance-first/module-last AHDL syntax;
- define `vdd=0.9`, `ACTUAL_GAIN=8.64`, `DITHER_AMP=0.014063`, `fs=50e6`,
  `fin=300e3`, and a small input perturbation/noise setting;
- provide a 50 MHz clock, active-low reset, and enable;
- connect `vin_src -> dither_adder -> gain_amp_fixed`, with `lfsr` driving
  dither sign `dpn`;
- run `tran tran stop=20u maxstep=8n`;
- save `vinp`, `vinn`, `vamp_p`, and `vamp_n`.

## Functional Contract

- `vin_src` should generate a deterministic post-reset differential input
  `vinp/vinn`.
- `lfsr` should generate repeatable one-bit voltage-domain dither on `dpn`.
- `dither_adder` should apply small positive/negative repeatable dither while
  preserving common-mode range.
- `gain_amp_fixed` should drive `vamp_p/vamp_n` as a fixed-gain differential
  output.
- Across many post-reset samples, output differential variation should be
  clearly larger than input differential variation and remain bounded in the
  `0 V` to `0.9 V` domain.

## Modeling Constraints

Use pure voltage-domain, event-driven Verilog-A. Use `@(cross(...))` for
clocked state updates where appropriate and smooth voltage transitions for
digital-like outputs. Do not use transistor-level devices, current-domain loads,
AC/noise analysis, file I/O, generated estimator modules, current
contributions, `ddt()`, or `idt()`.

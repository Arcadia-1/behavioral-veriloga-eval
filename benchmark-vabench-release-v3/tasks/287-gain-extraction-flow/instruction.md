# Gain Extraction Flow

Measurement L2 flow: build a voltage-domain dithered differential input path,
fixed-gain differential output path, and Spectre transient testbench. This is a
composed measurement/instrumentation flow for checking gain separation from a
small dithered input stimulus.

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
  `fin=300e3`, and a small deterministic input perturbation setting;
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

## Public Component Parameter And State Contracts

- `vin_src` defaults: `vdd = 0.9 V`, `vth = 0.45 V`, `ampl = 0.15 V`,
  `freq = 300 kHz`, `sigma = 0.01 V`, and `SEED = 0`. The testbench overrides
  `ampl`, `freq`, and `sigma` through its public parameters. On each rising
  `CLK` crossing after reset release, sample
  `vdd/2 + ampl*sin(2*pi*freq*t) + sigma*$rdist_normal(SEED, 0, 1)` onto
  `VOUT_P`; hold `VOUT_N` at `vdd/2`.
- `lfsr` default: `seed = 42`. On `initial_step` and on an active-low reset
  crossing of `RSTB`, initialize a 32-bit state from `seed`, force every fifth
  bit starting at bit 0 high for a nonzero startup pattern, and drive `DPN`
  from bit 31. On rising `CLK` while reset is released, shift toward higher bit
  indices with feedback `bit31 ^ bit21 ^ bit1 ^ bit0` into bit 0. Smooth `DPN`
  to the `VDD`/`VSS` rails with a `50 ps` transition.
- `dither_adder` defaults: `vdd = 0.9 V`, `vth = 0.45 V`, and
  `DITHER_AMP = 0.014063 V`. Split the selected differential dither equally
  around the input common-mode.
- `gain_amp_fixed` defaults: `vdd = 0.9 V` and `ACTUAL_GAIN = 8.64`. Center
  the differential output around `vdd/2`.

## Modeling Constraints

Use pure voltage-domain, event-driven Verilog-A. Use `@(cross(...))` for
clocked state updates where appropriate and smooth voltage transitions for
digital-like outputs. Do not use transistor-level devices, current-domain loads,
AC/noise analysis, file I/O, generated estimator modules, current
contributions, `ddt()`, or `idt()`.

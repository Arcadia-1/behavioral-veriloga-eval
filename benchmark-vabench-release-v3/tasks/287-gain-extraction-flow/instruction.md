# Gain Extraction Flow

## Task Contract
Build a measurement L2 flow for gain extraction from a dithered differential input path through a fixed-gain differential amplifier. The benchmark judges the composed source, dither, gain, and Spectre transient flow together.

## Public Verilog-A Interface
Return these scalar voltage-domain artifacts:

- `vin_src(CLK, RST_N, VOUT_P, VOUT_N)`
- `lfsr(DPN, VDD, VSS, CLK, EN, RSTB)`
- `dither_adder(VRES_P, VRES_N, DPN, VOUT_P, VOUT_N)`
- `gain_amp_fixed(VIN_P, VIN_N, VOUT_P, VOUT_N)`
- `tb_gain_extraction_ref.scs`

## Public Parameter Contract
The flow uses public testbench parameters such as `vdd=0.9`, `ACTUAL_GAIN=8.64`, `DITHER_AMP=0.014063`, a 50 MHz clock, active-low reset, and deterministic input perturbation settings. Component defaults should expose the same roles: source amplitude/frequency/noise seed, LFSR seed and reset, dither amplitude and threshold, and fixed amplifier gain.

## Required Behavior
`vin_src` generates a deterministic post-reset differential input. `lfsr` generates repeatable one-bit voltage-coded dither. `dither_adder` applies small positive or negative differential dither while preserving common-mode range. `gain_amp_fixed` centers and scales the differential output. Across many post-reset samples, output differential variation should be clearly larger than input differential variation and remain bounded in the `0 V` to `0.9 V` domain.

## Modeling Constraints
Use pure voltage-domain, event-driven Verilog-A and a portable Spectre deck with literal `ahdl_include` lines. Use `@(cross(...))` for clocked state updates where appropriate and smooth voltage transitions for digital-like outputs. Do not emit an estimator module, waveform files, private hooks, current-domain loads, transistor-level devices, AC/noise analysis, file I/O, current contributions, `ddt()`, or `idt()`.

## Output Contract
Return exactly `dither_adder.va`, `gain_amp_fixed.va`, `lfsr.va`, `tb_gain_extraction_ref.scs`, and `vin_src.va`. Do not return `gain_estimator.va`.

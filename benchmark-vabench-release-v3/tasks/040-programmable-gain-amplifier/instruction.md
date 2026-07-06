# Programmable Gain Amplifier

## Task Contract

Implement the requested Verilog-A artifact for `Programmable Gain Amplifier`.
- Form: `dut`
- Level: `L1`
- Category: `baseband_signal_conditioning`
- Target artifact(s): `programmable_gain_amplifier.va`

Implement `programmable_gain_amplifier.va` in Verilog-A.

Declare module `programmable_gain_amplifier(clk, rst, gain_sel, vin, out,
metric)` with all ports electrical. `clk`, `rst`, and `gain_sel` are
voltage-coded logic signals with a 0.45 V threshold. `vin` is an analog input
around `vcm`, `out` is the gain-scaled and bounded output, and `metric` marks
rail clipping.

Public parameters:

- `vth`: logic threshold, default `0.45`.
- `vcm`: common-mode voltage, default `0.45`.
- `gain_low`: gain selected when `gain_sel` is low, default `0.8`.
- `gain_high`: gain selected when `gain_sel` is high, default `2.4`.
- `vmin`: lower output clamp, default `0.0`.
- `vmax`: upper output clamp, default `0.9`.
- `tr`: output transition time, default `200p`.

Behavior:

- Initialize the selected gain to unity.
- Sample `gain_sel` on rising `clk` crossings and hold the selected gain
  between clock events.
- When `rst` is high, select unity gain, return `out` to `vcm`, and clear the
  clipping metric.
- Otherwise drive `out` from `vcm + gain * (V(vin) - vcm)`.
- Clamp `out` to `[vmin, vmax]`.
- Drive `metric` high only when the unclamped target would exceed either rail.

Modeling requirements:

- Use voltage contributions only; do not use current contributions,
  transistor-level devices, AC/noise analysis, or KCL/KVL assumptions.
- Use a sampled gain state and drive output voltages through `transition(...)`.
- Return only `programmable_gain_amplifier.va`; do not emit a Spectre
  testbench or validation harness.

## Public Verilog-A Interface

Declare module `programmable_gain_amplifier` with positional ports `clk, rst, gain_sel, vin, out, metric`. All ports are electrical. `clk`, `rst`, and `gain_sel` are voltage-coded control inputs, `vin` is the analog input around the common-mode level, `out` is the gain-scaled output, and `metric` indicates output clipping.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: logic threshold for `clk`, `rst`, and `gain_sel`.
- `vcm = 0.45 V`: input and output common-mode reference.
- `gain_low = 0.8`: sampled gain when `gain_sel` is low.
- `gain_high = 2.4`: sampled gain when `gain_sel` is high.
- `vmin = 0.0 V`: lower output clamp.
- `vmax = 0.9 V`: upper output clamp.
- `tr = 200 ps`: transition smoothing time for `out` and `metric`.

## Required Behavior

- Initialize the sampled gain to unity.
- On each rising `clk` crossing, sample `gain_sel` unless reset is active.
- While `rst` is above `vth`, use unity gain and drive `out` to `vcm`.
- When not reset, select `gain_high` for high `gain_sel` and `gain_low` for low `gain_sel`.
- Drive `out` as `vcm + gain * (V(vin) - vcm)` after clipping to the `vmin` to `vmax` range.
- Drive `metric` high when clipping occurs and low otherwise.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `programmable_gain_amplifier.va`. Do not include explanatory prose outside the source artifact contents.

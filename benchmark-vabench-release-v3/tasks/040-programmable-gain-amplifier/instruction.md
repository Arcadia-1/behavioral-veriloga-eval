# Programmable Gain Amplifier

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
  testbench or checker.

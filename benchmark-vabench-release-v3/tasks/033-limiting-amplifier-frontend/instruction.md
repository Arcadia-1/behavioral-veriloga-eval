# Limiting Amplifier Frontend

Implement `limiting_amplifier_frontend.va` in Verilog-A.

Declare module `limiting_amplifier_frontend(clk, rst, vin, out, metric)` with
all ports electrical. `clk` and `rst` are voltage-coded logic signals with a
0.45 V threshold. `vin` is an AFE input voltage centered around 0.45 V, `out`
is the bounded limiting-amplifier output, and `metric` marks limiting activity.

Public parameters:

- `tr`: output transition time, default `100p`.
- `vth`: logic threshold, default `0.45`.

Behavior:

- Initialize `out` to the 0.45 V common-mode level and `metric` low.
- Update the held output state on rising `clk` crossings.
- When `rst` is high, return the output to common mode and clear `metric`.
- For small excursions of `vin` around common mode, apply voltage gain above
  unity while preserving polarity.
- For large positive or negative excursions, limit the output toward bounded
  high and low levels instead of continuing linearly.
- Drive `metric` high only while large-signal limiting is active.
- Keep `out` and `metric` in the 0 V to 0.9 V voltage range.

Modeling requirements:

- Use voltage contributions only; do not use current contributions,
  transistor-level devices, AC/noise analysis, or KCL/KVL assumptions.
- Use a clocked state update and drive output voltages through
  `transition(...)`.
- Return only `limiting_amplifier_frontend.va`; do not emit a Spectre
  testbench or checker.

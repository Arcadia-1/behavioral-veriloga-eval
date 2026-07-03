# LNA Gain Compression Macro

Implement `lna_gain_compression_macro.va` in Verilog-A.

Declare module `lna_gain_compression_macro(clk, rst, vin, out, metric)` with
all ports electrical. `clk` and `rst` are voltage-coded logic signals with a
0.45 V threshold. `vin` is a receiver front-end input around 0.45 V common
mode, `out` is the amplified voltage, and `metric` indicates compression.

Public parameters:

- `tr`: output transition time, default `100p`.
- `vth`: logic threshold, default `0.45`.
- `gain`: small-signal voltage gain, default `2.2`.

Behavior:

- Initialize `out` to the 0.45 V common-mode level and `metric` low.
- Update the held output state on rising `clk` crossings.
- When `rst` is high, return the output to common mode and clear `metric`.
- In the small-signal region, apply the `gain` parameter to the deviation
  `V(vin) - 0.45`.
- For large positive and negative excursions, reduce incremental gain so the
  response compresses smoothly and remains bounded near the output rails.
- Keep compression roughly symmetric around common mode.
- Drive `metric` low or small in the linear region and high during compression.

Modeling requirements:

- Use voltage contributions only; do not use current contributions,
  transistor-level devices, AC/noise analysis, or KCL/KVL assumptions.
- Use a clocked state update and drive output voltages through
  `transition(...)`.
- Return only `lna_gain_compression_macro.va`; do not emit a Spectre testbench
  or checker.

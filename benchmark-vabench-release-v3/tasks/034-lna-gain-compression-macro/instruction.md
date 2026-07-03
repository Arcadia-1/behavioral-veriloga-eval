# LNA Gain Compression Macro

Implement `lna_gain_compression_macro.va` in Verilog-A.

## Public Interface

Declare module `lna_gain_compression_macro(clk, rst, vin, out, metric)`:

```verilog
module lna_gain_compression_macro(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

`clk` and `rst` are voltage-coded logic signals with low `0 V`, high `0.9 V`,
and threshold `0.45 V`. `vin` is a receiver front-end input around `0.45 V`
common mode. `out` is the amplified/compressed voltage. `metric` indicates
whether the macro is operating in compression.

## Public Parameter Contract

- `tr`: output transition time, default `100p`.
- `vth`: logic threshold, default `0.45`.
- `gain`: small-signal voltage gain, default `2.2`.

## Functional Contract

- Initialize `out` to the 0.45 V common-mode level and `metric` low.
- Update the held output state on rising `clk` crossings.
- When `rst` is high, return the output to common mode and clear `metric`.
- In the small-signal region, apply the `gain` parameter to the deviation
  `V(vin) - 0.45`.
- For large positive and negative excursions, reduce incremental gain so the
  response compresses smoothly and remains bounded near the output rails.
- Keep compression roughly symmetric around common mode.
- Drive `metric` low or small in the linear region and high during compression.

The visible testbench is a public verification scenario for wiring and saved
observables. Do not hard-code its transient stop time, waveform breakpoints, or
sample windows into the DUT.

## Modeling Constraints

Return only `lna_gain_compression_macro.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, transistor-level
devices, AC/noise analysis, or KCL/KVL assumptions. Use a clocked state update
and drive output voltages through `transition(...)`.

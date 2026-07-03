# Log RSSI Power Detector

Implement `log_rssi_power_detector.va` in Verilog-A.

Declare module `log_rssi_power_detector(clk, rst, vin, out, metric)` with all
ports electrical. `clk` and `rst` are voltage-coded logic signals with a
0.45 V threshold. `vin` is a received signal envelope around 0.45 V common
mode, `out` is a compressed RSSI-style voltage code, and `metric` exposes a
bounded envelope-magnitude estimate.

Public parameters:

- `tr`: output transition time, default `100p`.
- `vth`: logic threshold, default `0.45`.

Behavior:

- Initialize `out` near the low RSSI floor and `metric` low.
- Update the held RSSI state on rising `clk` crossings.
- When `rst` is high, return `out` to the low floor and clear `metric`.
- Estimate input amplitude from `abs(V(vin) - 0.45)`.
- Keep `out` monotonic with amplitude.
- Use a log-like or piecewise-compressed transfer: near-zero input should stay
  near the low floor, moderate input should move through the middle of the
  range, and larger input should increase with smaller incremental spacing.
- Keep `metric` proportional to envelope magnitude and bounded in the 0 V to
  0.9 V range.

Modeling requirements:

- Use voltage contributions only; do not use current contributions,
  transistor-level devices, AC/noise analysis, or KCL/KVL assumptions.
- Use Spectre/EVAS-friendly real arithmetic. Do not rely on unsupported
  `log10`, rounding, digital Verilog, or integer casts.
- Use a clocked state update and drive output voltages through
  `transition(...)`.
- Return only `log_rssi_power_detector.va`; do not emit a Spectre testbench or
  checker.

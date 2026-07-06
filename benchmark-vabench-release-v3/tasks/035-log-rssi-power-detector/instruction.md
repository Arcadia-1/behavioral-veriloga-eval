# Log RSSI Power Detector

## Task Contract

Implement the requested Verilog-A artifact for `Log RSSI Power Detector`.
- Form: `dut`
- Level: `L1`
- Category: `rf_afe_behavioral_macromodels`
- Target artifact(s): `log_rssi_power_detector.va`

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
  `log10`, rounding, digital Verilog, or integer casts.
- Use a clocked state update and drive output voltages through
  `transition(...)`.
- Return only `log_rssi_power_detector.va`; do not emit a Spectre testbench or
  validation.

## Public Verilog-A Interface

Declare module `log_rssi_power_detector` with positional ports `clk, rst, vin, out, metric`. All ports are electrical. `clk` and `rst` are voltage-coded control inputs, `vin` is the analog input around the common-mode level, `out` is the RSSI voltage, and `metric` is an amplitude-related observable.

## Public Parameter Contract

Provide these overrideable public parameters:

- `tr = 100 ps`: output transition rise/fall smoothing time.
- `vth = 0.45 V`: logic threshold for `clk` and `rst`.

## Required Behavior

- Initialize RSSI output to a low floor and `metric` low.
- On each rising `clk` crossing, sample the input magnitude unless reset is active.
- While `rst` is above `vth`, reset the RSSI output to the low floor and clear `metric`.
- Measure input magnitude as `abs(V(vin) - 0.45 V)`.
- Map increasing input magnitude to increasing piecewise RSSI levels, approximating a coarse logarithmic power detector.
- Keep the RSSI output bounded away from the rails.
- Drive `metric` as a bounded voltage proportional to the sampled input magnitude.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `log_rssi_power_detector.va`. Do not include explanatory prose outside the source artifact contents.

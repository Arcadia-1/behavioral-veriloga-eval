# Soft Hysteretic Limiter

Implement `soft_hysteretic_limiter.va` in Verilog-A.

## Public Interface

Declare module `soft_hysteretic_limiter(clk, rst, vin, out, metric)`:

```verilog
module soft_hysteretic_limiter(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

`clk` and `rst` are voltage-coded logic signals with low `0 V`, high `0.9 V`,
and threshold `0.45 V`. `vin` is the analog input. `out` is the conditioned
output voltage. `metric` is a voltage-coded hysteresis-state monitor.

## Public Parameter Contract

- `tr`: output transition smoothing time, default `100p`.
- `gain`: small-signal gain around the `0.45 V` common-mode level, default
  `1.8`.
- `hys_step`: signed hysteresis offset applied after upper/lower threshold
  excursions, default `0.08 V`.

## Functional Contract

- Implement a clocked soft limiter with hysteresis memory around the `0.45 V`
  common-mode level.
- Initialize the held output and state monitor near common mode.
- On each rising `clk` crossing, update the held limiter state. While `rst` is
  active high, reset the output and hysteresis state to their common-mode
  values.
- When reset is low, amplify the input deviation from common mode, add the
  current hysteresis offset, and bound the result inside the `0 V` to `0.9 V`
  signal range.
- A sufficiently high input excursion should set high-memory hysteresis; a
  sufficiently low input excursion should set low-memory hysteresis.
- During mid-level hold intervals, preserve the previous high or low memory
  state rather than collapsing immediately to a neutral state.
- Drive `metric` as a voltage-coded state monitor: above common mode for the
  high-memory state, below common mode for the low-memory state, and near common
  mode after reset.

The visible testbench is a public verification scenario for wiring and saved
observables. Do not hard-code its transient stop time, waveform breakpoints, or
sample windows into the DUT.

## Modeling Constraints

Return only `soft_hysteretic_limiter.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, transistor-level
devices, AC/noise analysis, `ddt()`, or `idt()`. Use event-updated state and
`transition(...)` for smoothed voltage outputs.

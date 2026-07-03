# Soft Hysteretic Limiter

Implement `soft_hysteretic_limiter.va` in Verilog-A.

## Public Interface

```verilog
module soft_hysteretic_limiter(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

All ports are scalar electrical voltage-domain ports. `clk` and `rst` are
voltage-coded logic signals with a `0.45 V` threshold. `rst` is active high.

## Public Parameter Contract

- `tr`: output transition smoothing time, default `100p`.
- `gain`: small-signal gain around the `0.45 V` common-mode level, default
  `1.8`.
- `hys_step`: signed hysteresis offset applied to the limiter state, default
  `0.08`.

## Functional Contract

- Model a baseband soft limiter with stateful hysteresis memory.
- Initialize `out` and `metric` near the midscale/common-mode state.
- On each rising `clk` crossing, reset the limiter to midscale while `rst` is
  active high.
- When reset is low, amplify `vin` around `0.45 V`, add the current hysteresis
  state, and bound `out` to the voltage signal range.
- A high `vin` excursion should move the limiter into a high-memory state with
  output compressed toward the upper limited region. A low `vin` excursion
  should move it into a low-memory state with output compressed toward the lower
  limited region.
- During mid-level hold windows, preserve the most recent high or low memory
  state rather than immediately returning to midscale.
- Drive `metric` as a voltage-coded hysteresis-state observable: high for the
  high-memory state, low for the low-memory state, and midscale after reset.

The visible testbench is a public verification scenario for wiring and saved
observables. Do not hard-code its transient stop time, waveform breakpoints, or
sample windows into the DUT.

## Modeling Constraints

Return only `soft_hysteretic_limiter.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, transistor-level
devices, AC/noise analysis, `ddt()`, or `idt()`.

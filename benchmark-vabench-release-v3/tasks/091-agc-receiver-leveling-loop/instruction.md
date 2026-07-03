# AGC Receiver Leveling Loop

Implement `agc_receiver_leveling_loop.va` in Verilog-A.

## Public Interface

```verilog
module agc_receiver_leveling_loop(clk, rst, vin, out, metric, gain_mon, rssi_mon);
input clk, rst, vin;
output out, metric, gain_mon, rssi_mon;
electrical clk, rst, vin, out, metric, gain_mon, rssi_mon;
```

All ports are scalar electrical voltage-domain ports. `clk` and `rst` are
voltage-coded logic signals with a `0.45 V` threshold. `rst` is active high.

## Public Parameter Contract

- `tr`: output transition smoothing time, default `100p`.
- `vth`: voltage-coded logic threshold, default `0.45`.
- `target_amp`: target output amplitude around common mode, default `0.18`.
- `deadband`: amplitude error band that avoids unnecessary gain updates,
  default `0.025`.

## Functional Contract

- Model a composed RF/AFE receiver AGC flow: gain path, envelope/RSSI
  observation, gain-control update, leveled output, and lock-quality metric.
- Treat `vin` as a receiver input envelope around `0.45 V` common mode.
- Initialize the gain control to a moderate gain, hold `out` near common mode,
  and clear the monitors while reset is active.
- On each rising `clk` crossing after reset, apply the current gain to
  `V(vin) - 0.45`, preserve common mode, and bound `out` to the signal range.
- Derive `rssi_mon` from the absolute output amplitude. Reduce gain when the
  observed amplitude is above `target_amp + deadband`; increase gain when it is
  below `target_amp - deadband`; keep the gain bounded.
- Drive `gain_mon` as a voltage-coded monitor of the bounded gain state.
- Drive `metric` high when the output amplitude is close to the AGC target and
  lower when the loop is far from target.

The visible testbench is a public verification scenario for wiring and saved
observables. Do not hard-code its transient stop time, waveform breakpoints, or
sample windows into the DUT.

## Modeling Constraints

Return only `agc_receiver_leveling_loop.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, transistor-level
devices, S-parameters, AC/noise analysis, `ddt()`, or `idt()`.

# RF Mixer Downconverter Macro

Implement `rf_mixer_downconverter_macro.va` in Verilog-A.

## Public Interface

```verilog
module rf_mixer_downconverter_macro(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

All ports are scalar electrical voltage-domain ports. `clk` is the LO-polarity
control waveform and `rst` is an active-high voltage-coded reset. Use a `0.45 V`
logic threshold where a digital decision is needed.

## Public Parameter Contract

- `tr`: output transition smoothing time, default `80p`.
- `vth`: voltage-coded logic threshold, default `0.45`.
- `conv_gain`: conversion gain applied to the input deviation from common mode,
  default `1.25`.

## Functional Contract

- Model a reusable voltage-domain RF/AFE mixer/downconverter macromodel, not a
  Spectre testbench or transistor-level RF circuit.
- Treat `vin` as an RF-envelope voltage around `0.45 V` common mode.
- While reset is active, hold `out` near common mode and clear `metric`.
- When reset is low, convert `V(vin) - 0.45` to a baseband output by multiplying
  it by LO polarity: high `clk` uses positive polarity and low `clk` uses
  negative polarity.
- Preserve the output common mode near `0.45 V`, apply `conv_gain`, and bound
  `out` to the voltage signal range.
- Drive `metric` as a voltage-coded activity observable that is low during
  reset and high when the conversion path is active.

The visible testbench is a public verification scenario for wiring and saved
observables. Do not hard-code its transient stop time, waveform breakpoints, or
sample windows into the DUT.

## Modeling Constraints

Return only `rf_mixer_downconverter_macro.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, transistor-level
devices, S-parameters, AC/noise analysis, `ddt()`, or `idt()`.

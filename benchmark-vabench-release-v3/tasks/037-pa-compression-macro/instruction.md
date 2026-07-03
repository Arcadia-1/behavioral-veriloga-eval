# PA Compression Macro

Implement `pa_compression_macro.va` in Verilog-A.

## Public Interface

Declare module `pa_compression_macro(clk, rst, vin, out, metric)`:

```verilog
module pa_compression_macro(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

`clk` and `rst` are voltage-coded logic signals with low `0 V`, high `0.9 V`,
and threshold `0.45 V`. `vin` is a PA drive voltage around `0.45 V` common
mode. `out` is the amplified output with large-signal compression. `metric`
marks compression or limiting operation.

## Public Parameter Contract

- `tr`: output transition time, default `100p`.
- `vth`: logic threshold, default `0.45`.
- `gain`: moderate-drive voltage gain, default `3.0`.

## Functional Contract

- Initialize `out` to the 0.45 V common-mode level and `metric` low.
- Update the held output state on rising `clk` crossings.
- When `rst` is high, return the output to common mode and clear `metric`.
- For moderate drive, apply gain above unity around common mode.
- For large positive and negative drive, compress the output toward bounded
  rail-adjacent limits rather than continuing linearly.
- Drive `metric` high when the PA output is in compression or near limiting.
- Keep `out` and `metric` in the 0 V to 0.9 V voltage range.

The visible testbench is a public verification scenario for wiring and saved
observables. Do not hard-code its transient stop time, waveform breakpoints, or
sample windows into the DUT.

## Modeling Constraints

Return only `pa_compression_macro.va`. Do not emit a Spectre testbench, checker
logic, private test hooks, or simulator-private side channels. Use voltage
contributions only; do not use current contributions, transistor-level devices,
RF S-parameters, AC/noise analysis, or KCL/KVL assumptions. Use a clocked state
update and drive output voltages through `transition(...)`.

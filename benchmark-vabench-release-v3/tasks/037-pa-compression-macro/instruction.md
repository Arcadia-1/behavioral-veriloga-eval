# PA Compression Macro

Implement `pa_compression_macro.va` in Verilog-A.

Declare module `pa_compression_macro(clk, rst, vin, out, metric)` with all
ports electrical. `clk` and `rst` are voltage-coded logic signals with a
0.45 V threshold. `vin` is a PA drive voltage around 0.45 V common mode, `out`
is the amplified output with large-signal compression, and `metric` marks
compression or limiting operation.

Public parameters:

- `tr`: output transition time, default `100p`.
- `vth`: logic threshold, default `0.45`.
- `gain`: moderate-drive voltage gain, default `3.0`.

Behavior:

- Initialize `out` to the 0.45 V common-mode level and `metric` low.
- Update the held output state on rising `clk` crossings.
- When `rst` is high, return the output to common mode and clear `metric`.
- For moderate drive, apply gain above unity around common mode.
- For large positive and negative drive, compress the output toward bounded
  rail-adjacent limits rather than continuing linearly.
- Drive `metric` high when the PA output is in compression or near limiting.
- Keep `out` and `metric` in the 0 V to 0.9 V voltage range.

Modeling requirements:

- Use voltage contributions only; do not use current contributions,
  transistor-level devices, RF S-parameters, AC/noise analysis, or KCL/KVL
  assumptions.
- Use a clocked state update and drive output voltages through
  `transition(...)`.
- Return only `pa_compression_macro.va`; do not emit a Spectre testbench or
  checker.

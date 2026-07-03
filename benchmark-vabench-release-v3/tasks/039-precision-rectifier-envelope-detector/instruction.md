# Precision Rectifier Envelope Detector

Implement `precision_rectifier_envelope_detector.va` in Verilog-A.

Declare module
`precision_rectifier_envelope_detector(clk, rst, vin, rect, env, metric)` with
all ports electrical. `clk` and `rst` are voltage-coded logic signals with a
0.45 V threshold. `vin` is an analog input around `vcm`, `rect` is the
full-wave rectified magnitude around common mode, `env` is a peak-envelope
state, and `metric` marks envelope hold memory.

Public parameters:

- `vth`: logic threshold, default `0.45`.
- `vcm`: rectifier common mode, default `0.45`.
- `decay`: envelope decay step per clock update, default `0.018`.
- `tr`: output transition time, default `150p`.

Behavior:

- Rectify the absolute deviation around common mode: zero input deviation maps
  `rect` to `vcm`, and either polarity of input excursion increases `rect`.
- Clip `rect` to the available 0 V to 0.9 V voltage range.
- Update `env` on rising `clk` crossings.
- When `rst` is high, return `env` to `vcm` and clear envelope memory.
- When the rectified input exceeds the stored envelope, update the envelope
  quickly to the new peak.
- When the rectified input falls below the stored envelope, let the envelope
  decay gradually while staying at or above the instantaneous rectified value
  and not falling below `vcm`.
- Drive `metric` high when `env` is holding materially above `rect`.

Modeling requirements:

- Use voltage contributions only; do not use current contributions,
  transistor-level devices, AC/noise analysis, or KCL/KVL assumptions.
- `rect` is a continuous rectified voltage expression and should be driven as a
  direct voltage contribution. `env` and `metric` are clocked states and should
  be driven through `transition(...)`.
- Return only `precision_rectifier_envelope_detector.va`; do not emit a Spectre
  testbench or checker.

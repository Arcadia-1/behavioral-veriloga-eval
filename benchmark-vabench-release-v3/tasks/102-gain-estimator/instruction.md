# Gain Estimator

Implement `gain_estimator.va` in Verilog-A.

## Interface

```verilog
module gain_estimator(VDD, VSS, vinp, vinn, voutp, voutn, gain_out, valid);
```

Ports:

- `VDD`, `VSS`: electrical supply/reference rails.
- `vinp`, `vinn`: electrical differential input being measured.
- `voutp`, `voutn`: electrical differential output being measured.
- `gain_out`: electrical voltage-coded gain metric.
- `valid`: electrical completion flag using the `VDD/VSS` logic range.

## Required Behavior

Write a pure voltage-domain gain measurement helper. After a configurable start
time, sample the input and output differential spans on a periodic timer. Once
the observed input span is large enough, report the span ratio as a normalized
voltage metric and assert `valid`.

Public parameters:

- `sample_period = 1 ns`: timer interval for span updates.
- `start_time = 20 ns`: time before samples begin contributing to the spans.
- `gain_scale = 10.0`: gain value represented by a full-scale `gain_out`.
- `min_input_span = 0.02 V`: minimum observed input span before the metric is
  considered valid.
- `tedge = 200 ps`: rise/fall smoothing for `gain_out` and `valid`.

Required observable behavior:

- Track minimum and maximum values of `V(vinp,vinn)` and `V(voutp,voutn)` after
  `start_time`.
- Compute input and output spans from those extrema.
- When input span exceeds `min_input_span`, set `gain = output_span/input_span`
  and assert `valid`.
- Drive `gain_out` as `V(VDD,VSS) * gain / gain_scale`.
- Drive `valid` low before the metric is valid and high afterwards.

Use event-updated real state for the measured gain and validity flag. Smooth
only discrete metric targets with `transition()`. Do not generate a Spectre
testbench, waveform files, checker artifacts, transistor-level devices, current
contributions, `ddt()`, or `idt()`.

## Output

Return exactly one complete Verilog-A file named `gain_estimator.va`.

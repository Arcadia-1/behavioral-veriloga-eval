# Acquisition Limited Sample And Hold

Implement `acquisition_limited_sample_hold.va` in Verilog-A.

## Public Interface

Declare module `acquisition_limited_sample_hold(sample, rst, vin, vout, metric)`
with scalar electrical voltage-domain ports.

- `sample`: voltage-coded acquisition-window control.
- `rst`: active-high voltage-coded reset.
- `vin`: analog input voltage.
- `vout`: acquired and held output voltage.
- `metric`: voltage-coded monitor that is high while the model is actively
  acquiring and low while it is holding or reset.

## Public Parameter Contract

- `vth`: logic threshold, default `0.45`.
- `vinit`: reset and initial held voltage, default `0.45`.
- `alpha`: acquisition fraction per update, default `0.42`.
- `tick`: acquisition update interval, default `1n`.
- `tr`: output and monitor transition smoothing time, default `200p`.

## Functional Contract

Model finite acquisition bandwidth rather than an ideal instantaneous sampler:

- A high `sample` level opens a tracking/acquisition window.
- While acquiring, `vout` moves toward the current `vin` voltage in discrete
  updates separated by `tick`.
- A falling `sample` crossing freezes the last acquired value.
- High `rst` returns the held output to `vinit` and clears the acquisition
  monitor.
- `metric` is high only while acquisition is active.

## Modeling Constraints

Return only `acquisition_limited_sample_hold.va`. Do not emit a Spectre
testbench, checker logic, private test hooks, or simulator-private side
channels. Use voltage contributions only; do not use current contributions,
`ddt()`, or `idt()`.

# Edge Crossing Interval Timer

Implement `cross_interval_163p333_ref.va` in Verilog-A.

## Interface

```verilog
module cross_interval_163p333_ref (
    inout  electrical VDD,
    inout  electrical VSS,
    input  electrical a,
    input  electrical b,
    output electrical delay_out,
    output electrical seen_out
);
```

## Required Behavior

This task asks for the `cross_interval_163p333_ref` behavioral DUT module, not
a Spectre testbench. The module measures the interval from a rising edge on
`a` to the next rising edge on `b` and exposes both the measured interval and a
completion marker.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `vth` | `0.45` | V | Rising-edge threshold for `a` and `b` relative to `VSS`. |
| `scale_ps` | `200.0` | ps, `(0:inf)` | Delay normalization used for `delay_out`. |
| `tedge` | `20 ps` | time, `(0:inf)` | Rise/fall smoothing for outputs. |

Required observable behavior:

- On a rising `a` crossing, arm a fresh measurement and clear the completion
  marker.
- On the first rising `b` crossing after the armed `a` edge, compute the elapsed
  time in picoseconds.
- Drive `delay_out` as `V(VDD,VSS) * measured_delay_ps / scale_ps`.
- Drive `seen_out` high after a valid `a`-then-`b` measurement and low while a
  measurement is armed but incomplete.
- Ignore additional `b` crossings until a new rising `a` edge starts the next
  measurement.

Use voltage-coded logic referenced to `VDD` and `VSS`, keep the model pure
behavioral Verilog-A, and do not use transistor-level devices, AC/noise
analysis, checker logic, private test hooks, or simulator-private side
channels.

## Output

Return exactly one source artifact named `cross_interval_163p333_ref.va`.

# RS Phase Detector

Implement `rs_phase_detector.va` in Verilog-A.

## Interface

```verilog
module rs_phase_detector(
    input  electrical ref,
    input  electrical fb,
    output electrical up,
    output electrical down
);
```

## Required Behavior

This task asks for the `rs_phase_detector` behavioral DUT module, not a Spectre
testbench. The module is an RS-latch style phase detector.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `vdd` | `1.2` | V, `(0:inf)` | High level for voltage-coded outputs and threshold reference. |
| `tdel` | `10 ps` | time, `[0:inf)` | Transition delay for outputs. |
| `tr` | `10 ps` | time, `(0:inf)` | Output rise time. |
| `tf` | `10 ps` | time, `(0:inf)` | Output fall time. |

Required observable behavior:

- Detect rising `ref` and `fb` crossings at `vdd / 2`.
- A rising `ref` edge sets the latch state so `up` is high and `down` is low.
- A rising `fb` edge resets the latch state so `up` is low and `down` is high.
- Hold the most recent latch state between qualifying input edges.
- Drive outputs as smoothed 0 V / `vdd` voltage-coded signals.

Use voltage contributions only. Do not use current contributions,
transistor-level devices, AC/noise analysis, checker logic, private test hooks,
or simulator-private side channels.

## Output

Return exactly one source artifact named `rs_phase_detector.va`.

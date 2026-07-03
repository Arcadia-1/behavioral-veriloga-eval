# Crossing Pulse Detector

Implement `source_crossing_pulse_detector.va` in Verilog-A.

## Interface

```verilog
module source_crossing_pulse_detector(
    input  electrical sigin,
    output electrical sigout
);
```

## Required Behavior

This task asks for the `source_crossing_pulse_detector` behavioral DUT module,
not a Spectre testbench. The module emits a fixed-width pulse when `sigin`
crosses the configured threshold in either direction.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `pulse_width` | `4 ns` | time, `(0:inf)` | Output high duration after a qualifying input crossing. |
| `sigcrossing` | `0.45` | V | Threshold for `sigin`. |
| `vlogic_high` | `0.9` | V | Output high level. |
| `vlogic_low` | `0.0` | V | Output low level. |
| `tdel` | `1 ns` | time, `[0:inf)` | Output transition delay. |
| `trise` | `20 ps` | time, `(0:inf)` | Output rise time. |
| `tfall` | `20 ps` | time, `(0:inf)` | Output fall time. |

Required observable behavior:

- Detect `sigin` crossings through `sigcrossing` in either direction.
- On each qualifying crossing, drive `sigout` high.
- Use a timer to return `sigout` low after `pulse_width`.
- Produce a pulse after each input crossing and return low between pulses.
- Drive `sigout` through smoothed voltage contributions.

Use voltage contributions only. Do not use current contributions, `ddt()`,
`idt()`, transistor-level devices, AC/noise analysis, checker logic, private
test hooks, or simulator-private side channels.

## Output

Return exactly one source artifact named `source_crossing_pulse_detector.va`.

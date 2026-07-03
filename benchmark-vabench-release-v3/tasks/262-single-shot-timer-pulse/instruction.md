# Single-Shot Timer Pulse

Implement `single_shot_timer_pulse.va` in Verilog-A.

## Interface

```verilog
module single_shot_timer_pulse(
    input  electrical vin,
    output electrical vout
);
```

## Required Behavior

This task asks for the `single_shot_timer_pulse` behavioral DUT module, not a
Spectre testbench. The module is a timer-based single-shot pulse generator.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `pulse_width` | `2 ns` | time, `(0:inf)` | Output high duration after a qualifying rising input edge. |
| `vlogic_high` | `0.9` | V | Output high level. |
| `vlogic_low` | `0.0` | V | Output low level. |
| `vtrans` | `0.45` | V | Rising-edge threshold for `vin`. |
| `tdel` | `100 ps` | time, `[0:inf)` | Output transition delay. |
| `trise` | `10 ps` | time, `(0:inf)` | Output rise time. |
| `tfall` | `10 ps` | time, `(0:inf)` | Output fall time. |

Required observable behavior:

- Detect rising `vin` crossings at `vtrans`.
- On each qualifying rising edge, drive `vout` high after the configured
  transition delay.
- Use a timer to return `vout` low after the configured pulse width.
- Generate one output pulse per input rising edge.
- Drive `vout` through smoothed voltage contributions.

Use voltage contributions only. Do not use current contributions,
transistor-level devices, AC/noise analysis, checker logic, private test hooks,
or simulator-private side channels.

## Output

Return exactly one source artifact named `single_shot_timer_pulse.va`.

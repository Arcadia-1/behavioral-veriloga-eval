# Single-Shot Pulse

Implement `source_single_shot.va` in Verilog-A.

## Interface

```verilog
module source_single_shot(
    input  electrical vin,
    output electrical vout
);
```

## Required Behavior

This task asks for the `source_single_shot` behavioral DUT module, not a Spectre
testbench. The module is a voltage-domain one-shot pulse generator.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `pulse_width` | `10 ns` | time, `(0:inf)` | Output high duration after a qualifying input edge. |
| `vlogic_high` | `0.9` | V | Output high level. |
| `vlogic_low` | `0.0` | V | Output low level. |
| `vtrans` | `0.45` | V | Rising-edge threshold for `vin`. |
| `tdel` | `1 ns` | time, `[0:inf)` | Output transition delay. |
| `trise` | `20 ps` | time, `(0:inf)` | Output rise time. |
| `tfall` | `20 ps` | time, `(0:inf)` | Output fall time. |

Required observable behavior:

- Detect rising `vin` crossings at `vtrans`.
- On each qualifying rising edge, drive `vout` high.
- Use a timer to return `vout` low after the configured pulse width.
- Generate one output pulse per input rising edge.
- Drive `vout` through smoothed voltage contributions.

Use voltage contributions only. Do not use current contributions, `ddt()`,
`idt()`, transistor-level devices, AC/noise analysis, checker logic, private
test hooks, or simulator-private side channels.

## Output

Return exactly one source artifact named `source_single_shot.va`.

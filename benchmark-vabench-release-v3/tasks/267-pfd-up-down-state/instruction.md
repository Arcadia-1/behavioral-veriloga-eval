# PFD Up/Down State

Implement `pfd_up_down_state.va` in Verilog-A.

## Interface

```verilog
module pfd_up_down_state(
    input  electrical ref,
    input  electrical fb,
    output electrical up,
    output electrical down
);
```

## Required Behavior

This task asks for the `pfd_up_down_state` behavioral DUT module, not a Spectre
testbench. The module is a bounded phase-frequency detector state machine.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `vdd` | `1.2` | V, `(0:inf)` | High level for voltage-coded outputs and threshold reference. |
| `tdel` | `10 ps` | time, `[0:inf)` | Transition delay for outputs. |
| `tr` | `10 ps` | time, `(0:inf)` | Output rise time. |
| `tf` | `10 ps` | time, `(0:inf)` | Output fall time. |

Required observable behavior:

- Detect rising `ref` and `fb` crossings at `vdd / 2`.
- Maintain an integer detector state bounded to `-1`, `0`, or `+1`.
- A rising `ref` edge increments the state up to `+1`.
- A rising `fb` edge decrements the state down to `-1`.
- Drive `up` high when the state is `+1`.
- Drive `down` high when the state is `-1`.
- Drive both outputs low when the state is `0`.

Use voltage contributions only. Do not use current contributions,
transistor-level devices, AC/noise analysis, checker logic, private test hooks,
or simulator-private side channels.

## Output

Return exactly one source artifact named `pfd_up_down_state.va`.

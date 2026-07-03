# Digital Phase Accumulator With Modulo Wrap

Implement `phase_accumulator_timer_wrap_ref.va` in Verilog-A.

## Interface

```verilog
module phase_accumulator_timer_wrap_ref (
    inout  electrical VDD,
    inout  electrical VSS,
    output electrical clk_out,
    output electrical phase_out
);
```

## Required Behavior

This task asks for the `phase_accumulator_timer_wrap_ref` behavioral DUT module,
not a Spectre testbench. The module is an ADPLL/NCO phase-timing primitive that
keeps a wrapped phase state and derives voltage-domain timing outputs.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `dt` | `5 ns` | time, `(0:inf)` | Timer update interval for the phase accumulator. |
| `phase_step` | `0.25` | normalized phase, `(0:1)` | Phase increment per timer update. |
| `tedge` | `200 ps` | time, `(0:inf)` | Rise/fall smoothing for `clk_out` and `phase_out`. |

Required observable behavior:

- Maintain a normalized phase state in `[0, 1)`.
- Advance the phase by `phase_step` on each `dt` timer event.
- Manually wrap phase back into `[0, 1)` instead of letting it grow unbounded.
- Drive `phase_out` as the wrapped phase scaled by the rail voltage
  `V(VDD,VSS)`.
- Drive `clk_out` as a rail-referenced voltage-coded clock derived from the
  wrapped phase.

Use voltage contributions only. Do not use current contributions, `ddt()`,
`idt()`, transistor-level devices, AC/noise analysis, checker logic, private
test hooks, or simulator-private side channels.

## Output

Return exactly one source artifact named `phase_accumulator_timer_wrap_ref.va`.

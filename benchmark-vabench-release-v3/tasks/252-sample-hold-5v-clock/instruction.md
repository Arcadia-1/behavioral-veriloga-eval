# Sample-Hold With 5 V Clock

Implement `sample_hold_5v_clock.va` in Verilog-A.

## Interface

```verilog
module sample_hold_5v_clock(
    input  electrical vin,
    output electrical vout,
    input  electrical vclk
);
```

## Required Behavior

This task asks for the `sample_hold_5v_clock` behavioral DUT module, not a
Spectre testbench. The module is an ideal voltage sample-and-hold controlled by
a 5 V clock.

Support this public parameter and legal override:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `vtrans_clk` | `2.5` | V | Rising-edge threshold for the 5 V sampling clock. |

Required observable behavior:

- Detect rising `vclk` crossings at `vtrans_clk`.
- At each qualifying clock edge, sample the instantaneous value of `vin`.
- Hold the sampled value on `vout` until the next qualifying clock edge.
- Do not update `vout` on falling clock edges.

Use voltage contributions only. Do not use current contributions,
transistor-level devices, AC/noise analysis, checker logic, private test hooks,
or simulator-private side channels.

## Output

Return exactly one source artifact named `sample_hold_5v_clock.va`.

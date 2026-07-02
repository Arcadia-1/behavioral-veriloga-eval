# Task Output Limiter

Implement one behavioral Verilog-A source file named `task_output_limiter.va`.

## Interface

Implement this exact interface:

```verilog
module task_output_limiter (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

Keep the model behavioral and do not introduce current contributions.

## Required Feature

Declare and call a Verilog-A task named `update_outputs` that accepts a real sample and an integer mode code. The task must update module-level `out_v` and `metric_v`.

## Required Behavior

Required task behavior:

- mode `0`: pass the sample through unchanged.
- mode `1`: output `vhi` when the sample is above `vth`, otherwise `0.0`.
- any other mode: clamp the sample into `[0.0, vhi]`.
- set `metric_v = out_v / vhi` after selecting `out_v`.

On every rising crossing of `clk`, reset all state to zero if `rst > vth`; otherwise increment `count_q`, set `state_q = count_q % 3`, and call `update_outputs(V(vin), state_q)`.

Return exactly one source artifact named `task_output_limiter.va`.

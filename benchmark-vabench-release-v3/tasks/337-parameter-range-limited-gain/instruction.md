# Parameter Range Limited Gain

Implement one behavioral Verilog-A DUT file named `parameter_range_limited_gain.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module parameter_range_limited_gain (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use a range-limited Verilog-A parameter declaration:

```verilog
parameter real gain_limited = 1.25 from [0.0:2.0];
```

Use voltage-coded logic with `vth = 0.45` V and high outputs limited to `vhi = 0.9` V.

On every rising crossing of `clk`:

1. If `rst` is high, drive both `out` and `metric` low.
2. Otherwise, compute an effective input equal to `vin` plus `0.20` V when `mode` is high.
3. Compute `raw = gain_limited * effective_input`.
4. Drive `metric` with this raw, pre-limit value.
5. Drive `out` with `raw` clipped to the range `[0.0, vhi]`.

The evaluator checks that the constrained parameter participates in the sampled gain, that `mode` can push the output into saturation, and that reset clears both outputs.

## Output

Return exactly one source artifact named `parameter_range_limited_gain.va`. Do not generate a Spectre testbench for this task.

# Port Connected Output Enable

## Task Contract

Implement one Verilog-A source file named `port_connected_output_enable.va`. The task models a clocked output-enable helper that uses `$port_connected` to guard an optional output port.

This is a DUT task. The supplied testbenches instantiate the connected-output path; the DUT should still define the unconnected optional-port behavior.

## Public Verilog-A Interface

Use this exact module interface, with the optional `out` port last:

```verilog
module port_connected_output_enable (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical metric,
    output electrical out
);
```

## Public Parameter Contract

Declare `parameter real vth = 0.45`, `parameter real vhi = 0.9`, and `parameter real tr = 200p`. `vth` is the clock and reset threshold, `tr` is the transition rise/fall time, and `vhi` is retained as a compatibility parameter.

## Required Behavior

Initialize `out`, `metric`, and the internal event counter to zero. On each rising crossing of `clk` through `vth`, reset those states when `rst > vth`; otherwise latch `V(vin)` as the selected output value and report `metric = 1.0` for the connected-output path.

## Modeling Constraints

Use `$port_connected(out)` in continuous analog context to derive whether the optional output is bound. When `out` is connected, drive `out` with the sampled input and drive `metric` high after valid clock samples. When `out` is not connected, keep `metric` at zero. Keep `transition(..., 0, tr, tr)` on the voltage contributions and use only voltage-domain contributions.

## Output Contract

Return exactly one source artifact named `port_connected_output_enable.va`.

# Parameter Range Limited Gain

## Task Contract

Implement one behavioral Verilog-A DUT file named `parameter_range_limited_gain.va`.

This task focuses on Cadence parameter range syntax in a sampled gain helper. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

## Form-Specific Requirements

Build a sampled voltage gain block that uses a range-limited Verilog-A parameter declaration as part of its public interface.

## Public Verilog-A Interface

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

## Public Parameter Contract

- Declare `parameter real gain_limited = 1.25 from [0.0:2.0];`.
- Use `vth = 0.45` V.
- Use high output level `vhi = 0.9` V.
- Use transition edge time `tr = 200p`.

## Required Behavior

- On each rising crossing of `V(clk) - vth`, update both outputs.
- If reset is high, clear both outputs to `0.0`.
- Otherwise compute `effective_input = V(vin) + 0.20` when `V(mode) > vth`, else `V(vin)`.
- Compute `raw = gain_limited * effective_input`.
- Drive `metric = raw`.
- Drive `out = raw` clipped to `0.0 ... vhi`.
- Smooth `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `parameter_range_limited_gain.va`. Do not generate a Spectre testbench for this task.

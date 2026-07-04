# Math Trig Envelope Detector

## Task Contract

Implement one behavioral Verilog-A DUT file named `math_trig_envelope_detector.va`.

This task focuses on sampled envelope behavior using `sin()`, `sqrt()`, and `abs()`. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

## Form-Specific Requirements

Build a clocked voltage-domain envelope helper that uses standard Verilog-A math functions in the sampled computation.

## Public Verilog-A Interface

```verilog
module math_trig_envelope_detector (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

- Use `vth = 0.45` V.
- Use high output level limit `vhi = 0.9` V.
- Use transition edge time `tr = 200p`.
- Use `pi = 3.141592653589793` or an equivalent accurate local constant.

## Required Behavior

- On each rising crossing of `V(clk) - vth`, update both outputs.
- If reset is high, clear both outputs to `0.0`.
- Otherwise compute `phase = 2*pi*V(vin)`.
- When mode is low, compute `out_sample = 0.45 + 0.25*sin(phase)`.
- When mode is high, compute `out_sample = 0.45 + 0.25*sin(phase - pi/2)`.
- Drive `out = out_sample` clipped to `0.0 ... vhi`.
- Drive `metric = sqrt(abs(out_sample))`.
- Smooth `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `math_trig_envelope_detector.va`. Do not generate a Spectre testbench for this task.

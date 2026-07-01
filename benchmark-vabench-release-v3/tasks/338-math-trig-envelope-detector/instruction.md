# Math Trig Envelope Detector

Implement one behavioral Verilog-A DUT file named `math_trig_envelope_detector.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

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

## Required Behavior

Use trigonometric and math functions in the behavior: `sin()`, `sqrt()`, and `abs()`.

Use voltage-coded logic with `vth = 0.45` V and high outputs below `vhi = 0.9` V.

On every rising crossing of `clk`:

1. If `rst` is high, drive both `out` and `metric` low.
2. Otherwise compute `phase = 2*pi*V(vin)`.
3. When `mode` is low, compute `out = 0.45 + 0.25*sin(phase)`.
4. When `mode` is high, compute `out = 0.45 + 0.25*sin(phase - pi/2)`.
5. Drive `metric = sqrt(abs(out))`.

The evaluator samples the low-mode sine envelope, the high-mode phase-shifted envelope, and reset clearing.

## Output

Return exactly one source artifact named `math_trig_envelope_detector.va`. Do not generate a Spectre testbench for this task.

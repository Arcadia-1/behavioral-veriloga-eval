# Limexp Soft Exponential

## Task Contract

Implement one behavioral Verilog-A source file named `limexp_soft_exponential.va`. This is a language-extension/L0 support task for the Spectre-compatible `limexp()` analog math operator on a sampled voltage-domain path, not a standalone diode or transistor-level device model.

Use `limexp(V(vin))` for the sampled transform. The limited exponential expression is the public modeling feature under review; keep the result observable through both `out` and `metric`.

## Public Verilog-A Interface

Use this exact module interface:

```verilog
module limexp_soft_exponential (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Use voltage-coded reset/clock threshold `vth = 0.45` V. Drive output transitions with rise/fall time `tr = 200p`. These values may be implemented as compatible Verilog-A parameters or internal constants.

## Required Behavior

- Initialize output state and `count_q` at `initial_step`.
- On each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high.
- Otherwise compute `out_v = limexp(V(vin))`.
- Set `metric_v = out_v`.
- Increment `count_q` after each non-reset sample.
- Drive `out` and `metric` with `transition(..., 0, tr, tr)`.

## Modeling Constraints

Keep the model behavioral and voltage-domain only. Do not introduce current contributions or broaden this row into a device-level current model.

## Output Contract

Return exactly one source artifact named `limexp_soft_exponential.va`.

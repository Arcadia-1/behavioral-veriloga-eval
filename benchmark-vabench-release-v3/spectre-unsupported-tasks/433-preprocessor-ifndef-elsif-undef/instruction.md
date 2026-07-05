# Preprocessor Ifndef Elsif Undef

## Task Contract

Implement one behavioral Verilog-A source file named `preprocessor_ifndef_elsif_undef.va`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module preprocessor_ifndef_elsif_undef (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
```

## Public Parameter Contract

Preserve these public parameter declarations and default values:

```verilog
parameter real vth = 0.45;
parameter real vhi = 0.9;
parameter real tr = 200p;
```

## Required Behavior

Use `ifndef, `elsif, and `undef to select a behavioral constant.

Required behavior:

- use preprocessor control with ``ifndef``, ``elsif``, and ``undef``;
- define `V3_GAIN_VALUE` as 0.75 when `V3_GAIN_MODE` is not defined;
- on each rising `clk` crossing, reset `out_v`, `metric_v`, and `count_q` when `rst` is high;
- otherwise drive `out_v = V3_GAIN_VALUE * V(vin)`;
- drive `metric_v = V3_GAIN_VALUE`;
- increment `count_q` after each non-reset sample;
- drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Do not add current-domain contributions unless the public interface explicitly requires them.

This row remains archived because it uses a preprocessor directive subset rejected by standalone Spectre in this environment. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `preprocessor_ifndef_elsif_undef.va`.

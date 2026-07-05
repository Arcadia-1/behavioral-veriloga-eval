# Task Output Limiter

## Task Contract

Implement one behavioral Verilog-A source file named `task_output_limiter.va`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module task_output_limiter (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
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

Required task behavior:

- mode `0`: pass the sample through unchanged.
- mode `1`: output `vhi` when the sample is above `vth`, otherwise `0.0`.
- any other mode: clamp the sample into `[0.0, vhi]`.
- set `metric_v = out_v / vhi` after selecting `out_v`.

On every rising crossing of `clk`, reset all state to zero if `rst > vth`; otherwise increment `count_q`, set `state_q = count_q % 3`, and call `update_outputs(V(vin), state_q)`.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Do not add current-domain contributions unless the public interface explicitly requires them.

This row remains archived because it uses a Verilog task/endtask declaration rejected by standalone Spectre in this environment. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `task_output_limiter.va`.

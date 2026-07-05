# Rdist T Tail Dither

## Task Contract

Implement one behavioral Verilog-A source file named `rdist_t_tail_dither.va`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module rdist_t_tail_dither (
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

Use `$rdist_t()` for deterministic seeded heavy-tail dither.

Required behavior:

- initialize `seed_q = 395`, `noise_q = 0.0`, `out_v = 0.0`, and `metric_v = 0.0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, and counters when `rst > vth`;
- otherwise draw `noise_q = $rdist_t(seed_q, 4.0)`;
- set `out_v = V(vin) + 0.01 * noise_q`;
- set `metric_v = noise_q`;
- drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Do not add current-domain contributions unless the public interface explicitly requires them.

This row remains archived because it uses a version-gated random distribution function rejected by the current Spectre environment. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `rdist_t_tail_dither.va`.

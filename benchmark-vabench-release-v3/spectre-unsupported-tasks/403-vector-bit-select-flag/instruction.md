# Vector Bit Select Flag

## Task Contract

Implement one behavioral Verilog-A source file named `vector_bit_select_flag.va`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module vector_bit_select_flag (
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

Use Verilog bit-select syntax on integer vector state.

Required behavior:

- initialize `count_q = 0`, `out_v = 0.0`, and `metric_v = 0.0`;
- on each rising crossing of `clk`, reset `out_v`, `metric_v`, `count_q`, and state when `rst > vth`;
- otherwise set `code_q = count_q + 4`;
- set `out_v = code_q[2] ? vhi : 0.0`;
- set `metric_v = code_q[0]`;
- increment `count_q` after computing the outputs;
- drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Do not add current-domain contributions unless the public interface explicitly requires them.

This row remains archived because it uses vector bit-select syntax rejected by standalone Spectre in this environment. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `vector_bit_select_flag.va`.

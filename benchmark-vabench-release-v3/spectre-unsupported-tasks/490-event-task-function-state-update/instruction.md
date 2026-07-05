# Event Task Function State Update

## Task Contract

Implement one behavioral Verilog-A source file named `event_task_function_state_update.va`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module event_task_function_state_update (input electrical clk, input electrical in, output electrical out);
```

## Public Parameter Contract

No public parameters are required for this archived row.

## Required Behavior

- Maintain an integer `count` and real state `q`.
- Define a user function `clamp01` that clamps a real value into `[0.0, 1.0]`.
- Define a task `update_state` with one real input `sample`.
- On every `cross(V(clk) - 0.45, +1)`, call `update_state(V(in))`.
- The task must increment `count` and set `q = clamp01(sample + 0.05 * count)`.
- Drive `out` with `q` using `transition(..., 0, 200p, 200p)`.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Do not add current-domain contributions unless the public interface explicitly requires them.

This row remains archived because it uses a Verilog task/endtask declaration rejected by standalone Spectre in this environment. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `event_task_function_state_update.va`.

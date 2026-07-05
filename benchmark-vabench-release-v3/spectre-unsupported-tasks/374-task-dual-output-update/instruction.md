# Task Dual Output Update

## Task Contract

Implement one behavioral Verilog-A source file named `task_dual_output_update.va`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module task_dual_output_update (
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

Use a task named `update_outputs` with two real inputs:

```verilog
task update_outputs;
    input real sample;
    input real trim;
```

On each rising crossing of `clk`, if `rst > vth`, reset both output states to zero. Otherwise call the task with `V(vin)` and `V(mode)`.

The task must compute:

- `out_v = clamp(sample + trim, 0.0, vhi)`
- `metric_v = clamp(sample - trim + 0.3, 0.0, vhi) / vhi`

Drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Do not add current-domain contributions unless the public interface explicitly requires them.

This row remains archived because it uses a Verilog task/endtask declaration rejected by standalone Spectre in this environment. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `task_dual_output_update.va`.

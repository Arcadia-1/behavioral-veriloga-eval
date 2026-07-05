# Task Local Variable Transform

## Task Contract

Implement one behavioral Verilog-A source file named `task_local_variable_transform.va`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module task_local_variable_transform (
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

Use a task with an internal local variable before updating output and metric state.

Required behavior:

- declare real state variables for `out_v` and `metric_v`;
- implement a task named `update_with_local` that takes a real sample and declares a local real variable such as `clipped`;
- inside the task, clamp the sample to the range 0.0 to 0.9;
- set `out_v` to the clipped value and `metric_v` to `clipped / 0.9`;
- initialize `out_v` and `metric_v` to 0.0 at `initial_step`;
- on each rising `clk` crossing, reset both values to 0.0 when `rst` is high;
- otherwise call the task with `V(vin)`;
- drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Do not add current-domain contributions unless the public interface explicitly requires them.

This row remains archived because it uses a Verilog task/endtask declaration rejected by standalone Spectre in this environment. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `task_local_variable_transform.va`.

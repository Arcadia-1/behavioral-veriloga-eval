# Task Stateful Threshold Update

## Task Contract

Implement one behavioral Verilog-A source file named `task_stateful_threshold_update.va`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module task_stateful_threshold_update (
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

Use a task named `threshold_update` to update state from thresholded analog inputs:

```verilog
task threshold_update;
    input real sample;
    input integer raise_mode;
```

Maintain a module-level real state `threshold_q`, initialized to `vth`. On each rising crossing of `clk`, reset `threshold_q` to `vth` and both outputs to zero if `rst > vth`; otherwise call `threshold_update(V(vin), V(mode) > vth)`.

The task must:

- compare `sample` against the current `threshold_q` before changing the threshold;
- drive `out_v = vhi` when `sample > threshold_q`, otherwise `0.0`;
- drive `metric_v = threshold_q`;
- when `raise_mode != 0`, increase `threshold_q` by `0.1` after the comparison, clamped to at most `0.75`.

Drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Do not add current-domain contributions unless the public interface explicitly requires them.

This row remains archived because it uses a Verilog task/endtask declaration rejected by standalone Spectre in this environment. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `task_stateful_threshold_update.va`.

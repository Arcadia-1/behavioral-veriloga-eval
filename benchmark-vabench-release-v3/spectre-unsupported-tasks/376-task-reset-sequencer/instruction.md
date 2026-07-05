# Task Reset Sequencer

## Task Contract

Implement one behavioral Verilog-A source file named `task_reset_sequencer.va`.

This is an archived Spectre-unsupported extension/support candidate. Keep the row non-counted in the default v3 denominator unless a future review explicitly restores it.

## Form-Specific Requirements

This is a single-source implementation task. Do not generate a Spectre testbench or auxiliary source files.

## Public Verilog-A Interface

Use this public interface or language construct:

```verilog
module task_reset_sequencer (
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

Use a task named `sequence_update` to share reset and normal update sequencing:

```verilog
task sequence_update;
    input real sample;
    input integer reset_active;
    input integer boost_mode;
```

On every rising crossing of `clk`, call `sequence_update(V(vin), V(rst) > vth, V(mode) > vth)`.

The task must:

- when `reset_active != 0`, set `phase_q = 0`, `out_v = 0.0`, and `metric_v = 0.0`;
- otherwise increment `phase_q`;
- set `out_v = sample + 0.2` when `boost_mode != 0`, otherwise `sample`;
- clamp `out_v` into `[0.0, vhi]`;
- set `metric_v = phase_q / 4.0` after a non-reset update.

Drive `out` and `metric` with `transition(...)`.

## Modeling Constraints

Keep the implementation behavioral and do not add transistor-level primitives.

Preserve the public module or construct names and the port order shown above.

Do not add current-domain contributions unless the public interface explicitly requires them.

This row remains archived because it uses a Verilog task/endtask declaration rejected by standalone Spectre in this environment. Do not restore or count it in the default v3 denominator without a separate human counting decision and fresh Spectre/AHDL evidence.

## Output Contract

Return exactly one source artifact named `task_reset_sequencer.va`.

# Reset Release Sequencer

Implement one Verilog-A source file named `reset_release_sequencer.va`.

## Task Contract

Build a Spectre-compatible voltage-domain behavioral model for Clocked reset-release sequencer for power and bias qualification before analog block startup.

## Form-Specific Requirements

This is a DUT source task. Implement only the `reset_release_sequencer` module; no external testbench, checker logic, transistor devices, or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module reset_release_sequencer(clk, rst, supply_ok, bias_ok, stage1, stage2, ready, progress);
```

## Public Parameter Contract

- `parameter real vth = 0.45`.
- `parameter real vhi = 0.9`.
- `parameter integer final_stage = 3`.
- `parameter real tr = 60p`.

## Required Behavior

- Release stage outputs in order on rising clock crossings.
- Require reset low, supply_ok high, and bias_ok high before advancing.
- Clear all stages on reset, supply fault, or bias fault.
- Assert ready only at the public final stage.
- Use local analog helper functions rather than user task/endtask syntax.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Do not use user `task`/`endtask`, Verilog-AMS digital kernels, branch current contributions, transistor devices, `ddt()`, or `idt()`. Do not hard-code visible or hidden stimulus times.

## Output Contract

Return only `reset_release_sequencer.va` implementing the public module. The file must compile under Spectre-compatible Verilog-A and must not require additional modules, include files beyond standard disciplines, or testbench changes.

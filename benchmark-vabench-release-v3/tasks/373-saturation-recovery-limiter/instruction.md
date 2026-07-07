# Saturation Recovery Limiter

Implement one Verilog-A source file named `saturation_recovery_limiter.va`.

## Task Contract

Build a Spectre-compatible voltage-domain behavioral model for Voltage-domain limiter that exposes saturation and recovery metrics for downstream analog signal conditioning.

## Form-Specific Requirements

This is a DUT source task. Implement only the `saturation_recovery_limiter` module; no external testbench, checker logic, transistor devices, or extra helper module is part of the requested artifact.

## Public Verilog-A Interface

```verilog
module saturation_recovery_limiter(vin, en, out, sat, recovery_metric);
```

## Public Parameter Contract

- `parameter real vth = 0.45`.
- `parameter real vhi = 0.9`.
- `parameter real vlo = 0.12`.
- `parameter real vlimit = 0.78`.
- `parameter real tr = 60p`.

## Required Behavior

- Clamp the enabled input between the public low and high limiter levels.
- Drive a saturation flag when either limiter boundary is active.
- Clear output, flag, and recovery metric while enable is low.
- Expose a bounded recovery metric proportional to clipped error.
- Use local analog functions rather than user task/endtask syntax.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Do not use user `task`/`endtask`, Verilog-AMS digital kernels, branch current contributions, transistor devices, `ddt()`, or `idt()`. Do not hard-code visible or hidden stimulus times.

## Output Contract

Return only `saturation_recovery_limiter.va` implementing the public module. The file must compile under Spectre-compatible Verilog-A and must not require additional modules, include files beyond standard disciplines, or testbench changes.

# Saturation Recovery Limiter

## Task Contract

Build a Spectre-compatible voltage-domain limiter that exposes saturation and recovery metrics for downstream analog signal conditioning.
- Form: `dut`.
- Level: `L1`.
- Category: voltage-domain analog signal conditioning.
- Target artifact: `saturation_recovery_limiter.va`.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

```verilog
module saturation_recovery_limiter(vin, en, out, sat, recovery_metric);
```

All ports are electrical. `vin` is the analog input, `en` is an active-high
voltage-coded enable, `out` is the limited output, `sat` is the saturation flag,
and `recovery_metric` reports normalized clipped error.

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
- Compute `limited = clamp(V(vin), vlo, vlimit)` while enabled and drive `out`
  to `limited`.
- Drive `sat = vhi` when enabled and `V(vin)` is outside `[vlo, vlimit]`;
  otherwise drive `sat = 0`.
- Drive the recovery metric as
  `recovery_metric = vhi * clip01(abs(V(vin) - limited) / (vlimit - vlo))`
  while enabled, and `0` while disabled.
- Use local analog functions rather than user task/endtask syntax.

## Modeling Constraints

Use voltage-domain behavioral Verilog-A only. Do not use user `task`/`endtask`, Verilog-AMS digital kernels, branch current contributions, transistor devices, `ddt()`, or `idt()`. Do not hard-code testbench-only stimulus times.

## Output Contract

Return only `saturation_recovery_limiter.va` implementing the public module. The file must compile under Spectre-compatible Verilog-A and must not require additional modules, include files beyond standard disciplines, or testbench changes.

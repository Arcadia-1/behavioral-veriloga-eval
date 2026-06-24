---
name: veriloga
description: Use when writing, fixing, or reviewing Verilog-A behavioral modules. Focuses on syntax, module/port discipline, state/event modeling, transition outputs, vector handling, and EVAS/Spectre portability. Does not provide circuit-specific recipes or simulation workflow.
---

# Verilog-A Syntax

Use this skill as a concise syntax and modeling-discipline checklist for
Verilog-A behavioral modules. Do not use it as a circuit cookbook. Do not run
simulation from this skill; use `evas-sim` only when visible/public EVAS
simulation is allowed.

## File And Module

- Write only the requested `.va` artifact(s).
- Preserve the exact filename, module name, port order, and public port names.
- Include standard headers:

```verilog
`include "constants.vams"
`include "disciplines.vams"
```

- Declare all ports/signals as `electrical`.
- Do not use SystemVerilog types: no `wire`, `logic`, `reg`, `always`, or
  `assign`.
- Use `inout` for supply ports such as `VDD`, `VSS`, `vdd`, `vss`.

## Declarations

- Put `parameter`, `real`, `integer`, and `genvar` declarations at module level,
  before `analog begin`.
- Initialize persistent state in `@(initial_step)`.
- Read supply levels from ports or parameters. Do not hardcode `0.9`, `1.2`, or
  `1.8` unless the task explicitly fixes them.
- Use the task's threshold when specified; otherwise use midpoint logic:

```verilog
vth = (vh + vl) / 2.0;
```

## Events And State

- Rising edge: `@(cross(V(clk) - vth, +1))`
- Falling edge: `@(cross(V(clk) - vth, -1))`
- Both edges: use two events or omit direction only when both are intended.
- Use `@(timer(...))` only for explicit timer-driven behavior.
- Keep event blocks for state updates; keep output contributions outside branch
  topology where possible.

## Output Contributions

- Drive voltage-domain outputs with `V(out) <+ transition(value, delay, rise);`.
- Compute output target values in `real` variables first.
- Contribute once per output node. Multiple contributions add; they do not
  overwrite.
- Avoid conditional contribution topology:

```verilog
// Prefer this
out_val = state ? vh : vl;
V(out) <+ transition(out_val, 0, trise);
```

```verilog
// Avoid this pattern
if (state) V(out) <+ transition(vh, 0, trise);
else V(out) <+ transition(vl, 0, trise);
```

## Ports And Vectors

ANSI-style example:

```verilog
module example (
  inout electrical VDD,
  inout electrical VSS,
  input electrical clk,
  output electrical [3:0] code
);
```

Old-style example:

```verilog
module example (VDD, VSS, clk, code);
inout VDD, VSS;
input clk;
output [3:0] code;
electrical VDD, VSS, clk;
electrical [3:0] code;
```

- Avoid body declarations like `inout electrical VDD, VSS;`; Spectre may reject
  them.
- Use `[MSB:LSB]` vector declarations, usually `[N-1:0]`.
- Use `integer` for runtime loops and `genvar` for repeated analog
  contributions.
- For Spectre portability, avoid runtime `integer` indexing of electrical buses
  in reads such as `V(code_i[k])`; unroll small buses when possible.

## Domain Boundaries

Prefer voltage-domain behavioral modeling for these benchmark tasks:

- `V(...) <+`
- `@(cross(...))`, `@(initial_step)`, `@(timer(...))`
- `transition(...)`
- sampled `real`/`integer` state

Avoid current-domain or continuous-time analog constructs unless explicitly
requested:

- `I(...) <+`
- `ddt`, `idt`, `idtmod`
- `laplace_*`
- `white_noise`, `flicker_noise`
- transistor-level or KCL/KVL solver assumptions

EVAS compatibility is not identical to Spectre compatibility. Write for the
task contract first, and keep syntax conservative.

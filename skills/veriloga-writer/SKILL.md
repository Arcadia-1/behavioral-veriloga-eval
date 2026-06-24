---
name: veriloga-writer
description: Use when writing, generating, fixing, or reviewing Verilog-A behavioral DUT modules for analog/mixed-signal tasks, especially voltage-domain benchmark artifacts. Covers module structure, electrical ports, supply handling, state initialization, edge detection, transition outputs, bus discipline, and EVAS/Spectre portability. Do not use for running simulation; use evas-sim for visible/public EVAS runs.
---

# Verilog-A Writer

Use this skill to write or fix Verilog-A behavioral DUT modules. Do not use it
to run simulation; visible/public EVAS simulation belongs to the separate
`evas-sim` skill.

## Scope

Write the requested `.va` module only. Do not generate hidden checks, verifier
logic, private testbenches, or extra wrapper files unless the task explicitly
asks for them.

Preserve exactly:

- required filename
- module name
- port order
- public port names
- requested parameters and observable names

## Mandatory Rules

Start portable Verilog-A files with:

```verilog
`include "constants.vams"
`include "disciplines.vams"
```

Use `electrical` for all signals. Do not use SystemVerilog types such as
`wire`, `logic`, or `reg`.

For power ports, use `inout`, not `input`.

Read supply levels from ports or parameters. Do not hardcode a supply such as
`1.8` or `0.9` unless the task explicitly fixes that value. Default logic
threshold is usually the midpoint:

```verilog
vth = (vh + vl) / 2.0;
```

Declare `parameter`, `real`, `integer`, and `genvar` at module level before
`analog begin`.

Initialize all persistent state in `@(initial_step)`.

Use `@(cross(expr, +1))` for rising edges and `@(cross(expr, -1))` for falling
edges. Omit the direction only when both edges are required.

Drive outputs once per node using `transition(...)`. Multiple contributions to
the same node add; they do not overwrite. Prefer:

```verilog
real out_val;
analog begin
  out_val = state ? vh : vl;
  V(out) <+ transition(out_val, 0, trise);
end
```

Avoid conditional analog contribution topology such as placing
`V(out) <+ transition(...)` only inside one branch. Compute the value first,
then contribute unconditionally.

## Ports And Buses

ANSI-style, one port per line:

```verilog
module example (
  inout electrical VDD,
  inout electrical VSS,
  input electrical clk_i,
  output electrical [3:0] dout_o
);
```

Old-style separated declaration:

```verilog
module example (VDD, VSS, clk_i, dout_o);
inout VDD, VSS;
input clk_i;
output [3:0] dout_o;
electrical VDD, VSS, clk_i;
electrical [3:0] dout_o;
```

Avoid body declarations like `inout electrical VDD, VSS;`; Spectre may reject
this. In ANSI style, do not rely on `electrical` carrying across a comma.

For vector ports, use `[MSB:LSB]`, usually `[N-1:0]`.

Use `integer` for runtime/procedural loops that update variables. Use `genvar`
for repeated analog contributions. For Spectre portability, do not use a
runtime `integer` loop variable to index an electrical bus inside procedural
reads like `V(code_i[k])`; unroll small buses explicitly or restructure.

## Domain Classification

Voltage-domain behavioral models usually use:

- `V(...) <+`
- event logic such as `@(cross(...))`
- `transition(...)`
- sampled real/integer state

Current-domain or continuous-time analog models use constructs such as:

- `I(...) <+`
- `ddt(...)`, `idt(...)`, `laplace_*`
- transistor-level/KCL behavior

For this benchmark, prefer voltage-domain behavioral models unless the task
explicitly asks for current-domain behavior.

If a module mixes voltage-domain control and current-domain analog behavior,
split responsibilities if the task allows it. Otherwise state the limitation
clearly.

## EVAS Compatibility Notes

EVAS can check voltage-domain event-driven Verilog-A. To keep code EVAS-friendly:

- Prefer `V(node) <+ transition(value, delay, rise)` style outputs.
- Use explicit event-driven state updates.
- Avoid `I() <+`, `ddt`, `idt`, `laplace`, noise sources, and transistor-level
  constructs.
- Avoid Spectre-hostile runtime electrical-bus indexing if Cadence/Spectre
  compatibility matters.

EVAS compatibility is not the same as Spectre compatibility. Write for the task
contract first.

## Output Discipline

Return only the requested artifact content or edit only the requested file(s).
Do not include prose inside generated source files unless comments are useful
and concise.

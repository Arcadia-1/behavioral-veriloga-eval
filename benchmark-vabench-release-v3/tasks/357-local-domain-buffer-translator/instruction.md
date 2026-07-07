# Local Domain Buffer Translator

Implement one Verilog-A source file named `local_domain_buffer_translator.va`.

## Task Contract

Build a voltage-domain analog/mixed-signal helper or monitor. Local-domain voltage translator that maps a rail-referenced input into a global voltage-coded output.

## Public Verilog-A Interface

```verilog
module local_domain_buffer_translator(in0, in1, in2, in3, ctrl0, ctrl1, vdd, vss, en, out, flag, metric);
```

All ports are electrical. `vdd` and `vss` are the local rails, `en` is an
active-high enable, `in0` through `in3` are voltage-coded analog or lane inputs,
`ctrl0` and `ctrl1` are voltage-coded control inputs, and `out`, `flag`, and
`metric` are voltage-coded observables.

## Public Parameter Contract

- `vth = 0.45 V`: logic threshold for voltage-coded controls.
- `vhi = 0.9 V`: high level for output observables.
- `span_min = 0.62 V`, `span_max = 1.28 V`: legal local supply span measured as
  `V(vdd, vss)`.
- `tr = 50p`: output transition smoothing time.

## Required Behavior

Measure analog inputs relative to the local `vss` rail and normalize by the
current local supply span. Let `span = V(vdd, vss)` and treat the row as valid
only when `V(en) > vth` and `span_min <= span <= span_max`; otherwise drive
`out`, `flag`, and `metric` to `0 V`. If `span` is below `0.05 V`, use
`0.05 V` as the normalization span. Define `clip01(y)` as `y` limited to the
range `[0, 1]`, `x0 = clip01((V(in0) - V(vss)) / span)`, and
`c1 = clip01(V(ctrl1) / vhi)`.

Translate the local input with `core = 0.76 * x0 + 0.18 * c1 + 0.12` and drive
`out = vhi * clip01(core)` while valid. Assert `flag = vhi` when the local
supply span is at least `0.78 V`, otherwise drive `flag = 0 V`. Drive
`metric = vhi * clip01(abs((V(in0) - V(vss)) - 0.5 * span) / span)` as the
bounded distance from the half-span input point.

## Modeling Constraints

Use Spectre-compatible voltage-domain Verilog-A. Do not use unsupported
`wreal`, `logic`, `assign`, `always`, `task/endtask`, `connectmodule`,
`connectrules`, `specify`, `generate`, recursion, packed logic buses, or
multidimensional array syntax. Do not generate a testbench, checker logic,
current contributions, transistor devices, `ddt()`, or `idt()`.

## Output Contract

Return only `local_domain_buffer_translator.va` implementing the public module. The file must
compile under Spectre-compatible Verilog-A and must not require additional
modules, nonstandard include files, or testbench changes.

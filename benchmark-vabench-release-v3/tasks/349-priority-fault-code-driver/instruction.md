# Priority Fault Code Driver

Implement one Verilog-A source file named `priority_fault_code_driver.va`.

## Task Contract

Build a voltage-domain analog/mixed-signal helper or monitor. Priority fault encoder for supply, bias, reset, and mode faults using voltage-coded outputs.

## Public Verilog-A Interface

```verilog
module priority_fault_code_driver(in0, in1, in2, in3, ctrl0, ctrl1, vdd, vss, en, out, flag, metric);
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
range `[0, 1]`, `x0..x3 = clip01((V(inN) - V(vss)) / span)`, and
`c0 = clip01(V(ctrl0) / vhi)`.

Encode the highest-priority fault code using this order: if `x0 > 0.58`, use
code `0.25`; else if `x1 > 0.58`, use code `0.50`; else if `x2 > 0.58`, use
code `0.75`; else if `c0 > 0.58`, use code `1.0`; otherwise use code `0.0`.
Drive `out = vhi * clip01(code)` and `metric = vhi * clip01(code)`. Assert
`flag = vhi` when `code >= 0.50`, otherwise drive `flag = 0 V`.

## Modeling Constraints

Use Spectre-compatible voltage-domain Verilog-A. Do not use unsupported
`wreal`, `logic`, `assign`, `always`, `task/endtask`, `connectmodule`,
`connectrules`, `specify`, `generate`, recursion, packed logic buses, or
multidimensional array syntax. Do not generate a testbench, checker logic,
current contributions, transistor devices, `ddt()`, or `idt()`.

## Output Contract

Return only `priority_fault_code_driver.va` implementing the public module. The file must
compile under Spectre-compatible Verilog-A and must not require additional
modules, nonstandard include files, or testbench changes.

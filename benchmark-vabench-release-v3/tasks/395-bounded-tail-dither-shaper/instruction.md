# Bounded Tail Dither Shaper

## Task Contract

Build a voltage-domain analog/mixed-signal helper or monitor: a bounded tail-like dither shaper using deterministic rail-coded inputs instead of unsupported t-distribution sampling.
- Form: `dut`.
- Level: `L1`.
- Category: deterministic dither/monitor helper.
- Target artifact: `bounded_tail_dither_shaper.va`.
- Output boundary: implement only the requested public Verilog-A DUT artifact.

## Public Verilog-A Interface

```verilog
module bounded_tail_dither_shaper(clk, rst, in0, in1, in2, in3, ctrl0, ctrl1, vdd, vss, en, out, flag, metric);
```

All ports are electrical. `vdd` and `vss` are the local rails, `en` is an
active-high enable, `in0` through `in3` are voltage-coded analog or lane inputs,
`ctrl0` and `ctrl1` are voltage-coded control inputs, and `out`, `flag`, and
`metric` are voltage-coded observables. For clocked rows, `clk` is the sampling
clock and `rst` clears the observable state.

## Public Parameter Contract

- `vth = 0.45 V`: logic threshold for voltage-coded controls.
- `vhi = 0.9 V`: high level for output observables.
- `span_min = 0.62 V`, `span_max = 1.28 V`: legal local supply span measured as
  `V(vdd, vss)`.
- `tr = 50p`: output transition smoothing time.

## Required Behavior

Measure analog inputs relative to the local `vss` rail and normalize by the
current local supply span `span = V(vdd, vss)`. Clear all observables when `en`
is low or when `span` is outside `[span_min, span_max]`. The DUT updates its
observable state on rising `clk` crossings and clears state while `rst` is high.

For each valid update, compute:

```text
x0 = clip01((V(in0) - V(vss)) / span)
x1 = clip01((V(in1) - V(vss)) / span)
c0 = clip01(V(ctrl0) / vhi)
aux = clip01(abs(x0 - x1) + 0.35*c0)
acc = clip01(0.62*previous_acc + 0.32*aux)
out = vhi*acc
flag = vhi when acc > 0.58, otherwise 0
metric = vhi*aux
```

Reset, disabled, and out-of-range supply conditions set `previous_acc`, `out`,
`flag`, and `metric` to 0. Preserve `in2`, `in3`, and `ctrl1` as public
interface inputs; they are not part of the bounded-tail update formula for this
task.

## Modeling Constraints

Use Spectre-compatible voltage-domain Verilog-A. Do not use unsupported
`wreal`, `logic`, `assign`, `always`, `task/endtask`, `connectmodule`,
`connectrules`, `specify`, `generate`, recursion, packed logic buses, or
multidimensional array syntax. Do not generate a testbench, checker logic,
current contributions, transistor devices, `ddt()`, or `idt()`.

## Output Contract

Return only `bounded_tail_dither_shaper.va` implementing the public module. The file must
compile under Spectre-compatible Verilog-A and must not require additional
modules, nonstandard include files, or testbench changes.

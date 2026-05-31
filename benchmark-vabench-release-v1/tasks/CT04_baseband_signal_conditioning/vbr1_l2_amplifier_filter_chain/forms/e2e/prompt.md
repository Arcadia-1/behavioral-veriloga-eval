# Task: vbr1_l2_amplifier_filter_chain:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Baseband Signal Conditioning
- Base function: Amplifier/filter chain
- Domain: `voltage`
- Target artifact(s): `amplifier_filter_chain.va`, `tb_amplifier_filter_chain.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## L2 Background And Claim Boundary

This Level-2 row is a behavioral composition/flow task for Amplifier/filter chain. It should expose intermediate state, multi-stage behavior, or a closed-loop relation through the public observables below.
Stay within the listed voltage-domain/event-driven contract. Do not use transistor-level devices, current-domain loads, AC/noise analysis, S-parameters, or hidden checker logic unless the public contract explicitly lists them.
Paper-facing claims for this row are limited to the public behavior checks below; do not broaden the task into full silicon implementation, layout, device physics, or unlisted performance metrics.

## Form-Specific Requirements

- Generate all target artifacts: `amplifier_filter_chain.va`, `tb_amplifier_filter_chain.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.
- The generated Verilog-A file(s) `amplifier_filter_chain.va` must be co-located with the generated Spectre testbench.
- Include the generated DUT exactly with `ahdl_include "amplifier_filter_chain.va"` in the generated testbench.
- Use Spectre AHDL instance syntax with the instance name first and module name last: `XNAME (node1 node2 ...) module_name`.
- Never write module-first syntax such as `module_name instance_name (...)`; that is not the release Spectre testbench syntax.

## Public Verilog-A Interface

- `amplifier_filter_chain.va` declares module `amplifier_filter_chain` with positional ports: `clk`, `rst`, `vin`, `out`, `metric`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=80n maxstep=0.5n
```

The release harness expects these exact public scalar observables:

- `clk`
- `rst`
- `vin`
- `out`
- `metric`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `clk`
- `rst`
- `vin`

## Public Spectre Testbench Scaffold

When this form generates a `.scs` testbench, use the following public skeleton shape. Fill in only the public stimulus details required by the task; do not copy or emit hidden checker logic.

```spectre
simulator lang=spectre
global 0
ahdl_include "amplifier_filter_chain.va"

XDUT (clk rst vin out metric) amplifier_filter_chain

tran tran stop=80n maxstep=0.5n
save clk rst vin out metric
```

Critical syntax rules:

- Every Verilog-A DUT/support file used by the testbench must have a literal `ahdl_include "<file>.va"` line in the `.scs` artifact.
- Spectre AHDL instances use instance-first/module-last syntax: `XNAME (node1 node2 ...) module_name`.
- Do not use module-first syntax such as `module_name instance_name (...)`.
- Keep saved names as plain scalar public observables, not instance-qualified aliases.

## Public Behavior Checks

- `amplified_input`
- `filtered_output_lags_input`
- `metric_tracks_settling`

## Public L2 Behavior Contract

Implement the chain as two visible behavioral stages:

1. Gain stage:
   - Compute a bounded amplified target from `vin`.
   - Expose this pre-filter target on `metric`.

2. Filter stage:
   - Drive `out` as a lagged low-pass response toward `metric`, not as an
     instantaneous copy.
   - Keep both `out` and `metric` bounded in the 0 V to 0.9 V signal range.
   - Put clocked updates in a top-level `@(cross(V(clk) - 0.45, +1))` event
     block. Do not place `@(cross(...))` inside an `if/else` branch; put reset
     and branch logic inside the event body instead.

The public testbench should apply a low-to-high input step and run long enough
for `metric` to move first and `out` to visibly lag before settling.

Use a compact public stimulus schedule that exposes high, midscale, and low
targets:

- Release reset before 8 ns and drive logic high as 0.9 V.
- High target: drive `vin` high enough that the bounded gain-stage target
  (`metric`) is near 0.9 V through the 12.5-15 ns and 24-28 ns windows; `out`
  should lag early and settle upward later.
- Mid target: drive `vin` so `metric` is near 0.45 V through the 33-36 ns
  window.
- Low target: drive `vin` so `metric` is near 0 V through the 46-55 ns window,
  and let `out` fall by the 54-58 ns window.
- The expected public relation is: `metric` jumps quickly to the pre-filter
  target, while `out` moves gradually. In the early high window, `metric` should
  exceed `out` by a visible margin; in the later high window, `out` should have
  increased toward `metric`.
- Use parenthesized Spectre source syntax and the analysis line exactly as
  `tran tran stop=80n maxstep=0.5n`.
- PWL timestamps must be strictly increasing. Do not repeat a timestamp for an
  instantaneous step; instead use a short positive transition interval such as
  30.0 ns to 30.1 ns.
- Hold each input value stable across its measurement window rather than
  ramping through that window.

## Output Contract

Return exactly these source artifacts:

- `amplifier_filter_chain.va`
- `tb_amplifier_filter_chain.scs`

Return each artifact as a separate fenced code block, with the Verilog-A block
first and the Spectre testbench block second. Do not omit either artifact,
rename files, or include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

### Amplifier/filter chain (end-to-end)

Write both the Verilog-A behavioral module and a Spectre transient testbench.

Behavioral intent:

Combine a gain block and low-pass filter; expose the bounded pre-filter amplified target on metric so out can be checked for lagged settling.

Module name: `amplifier_filter_chain`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module amplifier_filter_chain(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. out is the bounded filtered voltage. metric exposes the bounded pre-filter amplified target used to verify that out lags and settles toward the amplified input.

Saved waveform columns:

```text
clk rst vin out metric
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

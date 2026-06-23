# Task: metastability_window_comparator:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Comparator and Decision Circuits
- Base function: Comparator metastability window model
- Domain: `voltage`
- Target artifact(s): `metastability_window_comparator.va`, `tb_metastability_window_comparator.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## L2 Background And Claim Boundary

This Level-2 row is a behavioral composition/flow task for Comparator metastability window model. It should expose intermediate state, multi-stage behavior, or a closed-loop relation through the public observables below.
Stay within the listed voltage-domain/event-driven contract. Do not use transistor-level devices, current-domain loads, AC/noise analysis, S-parameters, or hidden checker logic unless the public contract explicitly lists them.
Paper-facing claims for this row are limited to the public behavior checks below; do not broaden the task into full silicon implementation, layout, device physics, or unlisted performance metrics.

## Form-Specific Requirements

- Generate all target artifacts: `metastability_window_comparator.va`, `tb_metastability_window_comparator.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.
- The generated Verilog-A file(s) `metastability_window_comparator.va` must be co-located with the generated Spectre testbench.
- Include the generated DUT exactly with `ahdl_include "metastability_window_comparator.va"` in the generated testbench.
- Use Spectre AHDL instance syntax with the instance name first and module name last: `XNAME (node1 node2 ...) module_name`.
- Never write module-first syntax such as `module_name instance_name (...)`; that is not the release Spectre testbench syntax.

## Public Verilog-A Interface

- `metastability_window_comparator.va` declares module `metastability_window_comparator` with positional ports: `in`, `clk`, `rst`, `out`, `metric`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=260n maxstep=500p
```

Public stimulus/source nodes visible in the reference harness include:

- `clk`
- `rst`
- `in`

## Public Spectre Testbench Scaffold

When this form generates a `.scs` testbench, use the following public skeleton shape. Fill in only the public stimulus details required by the task; do not copy or emit hidden checker logic.

```spectre
simulator lang=spectre
global 0
ahdl_include "metastability_window_comparator.va"

Xdut (in clk rst out metric) metastability_window_comparator

tran tran stop=260n maxstep=500p
```

Critical syntax rules:

- Every Verilog-A DUT/support file used by the testbench must have a literal `ahdl_include "<file>.va"` line in the `.scs` artifact.
- Spectre AHDL instances use instance-first/module-last syntax: `XNAME (node1 node2 ...) module_name`.
- Do not use module-first syntax such as `module_name instance_name (...)`.
- Keep saved names as plain scalar public observables, not instance-qualified aliases.

## Public Behavior Checks

- `metastability_window_comparator_full_behavior`
- `windowed_decision_flow_near_miss_rejection`

## Output Contract

Return exactly these source artifacts:

- `metastability_window_comparator.va`
- `tb_metastability_window_comparator.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: metastability_window_comparator:e2e

## vaBench-300 v1.1 Task-Specific Contract

- Status: `provisional_v1.1_management`
- Paper score: `disabled_until_fresh_spectre_certification`
- Form: `e2e`
- Family: `end-to-end`
- Level: `L2`
- Track: `core`
- Difficulty: `D3`
- Category: Comparator and Decision Circuits
- Base function target: Comparator metastability window model
- Domain: voltage-domain behavioral Verilog-A

This row has been rebuilt from the original v1.1 management scaffold into
a task-specific benchmark candidate. It remains outside the paper score
denominator until fresh EVAS/Spectre certification is recorded for this
rebuilt source asset.

## Current Public Interface

- Verilog-A artifact: `metastability_window_comparator.va`
- Spectre testbench artifact: `tb_metastability_window_comparator.scs`
- Module name: `metastability_window_comparator`
- Positional ports: `in`, `clk`, `rst`, `out`, `metric`
- Port roles:
  - `in`: voltage-coded stimulus input.
  - `clk`: voltage-coded event clock, low=0 V and high=1 V.
  - `rst`: voltage-coded reset pulse.
  - `out`: bounded state/output monitor.
  - `metric`: derived state metric monitor.

## Task-Specific Observable Contract

- Behavior: clocked comparator whose decision confidence degrades near the differential threshold window.
- Observable: out is the resolved comparator decision; metric is high inside the metastability window.
- Checker: near-threshold samples produce larger metric values than far-from-threshold samples.
- Rising `rst` clears state before the measurement window.
- Rising `clk` events drive the discrete-time behavior.
- The Spectre scaffold instantiates the DUT with instance-first AHDL syntax
  and records `time`, `in`, `clk`, `rst`, `out`, and `metric`.

## Task Goal

Create the model and latency-measurement flow.

Do not satisfy this task with a generic state scaffold. The implementation
must preserve the named circuit-function behavior and expose both the
`out` waveform and the task-specific `metric` monitor.

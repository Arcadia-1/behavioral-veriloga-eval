# Task: metastability_window_comparator:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L2`
- Category: Comparator and Decision Circuits
- Base function: Comparator metastability window model
- Domain: `voltage`
- Target artifact(s): `metastability_window_comparator.va`
- Supplied/reference support artifact(s): `tb_metastability_window_comparator.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## L2 Background And Claim Boundary

This Level-2 row is a behavioral composition/flow task for Comparator metastability window model. It should expose intermediate state, multi-stage behavior, or a closed-loop relation through the public observables below.
Stay within the listed voltage-domain/event-driven contract. Do not use transistor-level devices, current-domain loads, AC/noise analysis, S-parameters, or hidden checker logic unless the public contract explicitly lists them.
Paper-facing claims for this row are limited to the public behavior checks below; do not broaden the task into full silicon implementation, layout, device physics, or unlisted performance metrics.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `metastability_window_comparator.va` declares module `metastability_window_comparator` with positional ports: `in`, `clk`, `rst`, `out`, `metric`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=260n maxstep=500p
```


## Public Behavior Checks

- `metastability_window_comparator_full_behavior`
- `window_boundary_bug_near_miss_rejection`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `metastability_window_comparator.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: metastability_window_comparator:bugfix

## vaBench-300 v1.1 Task-Specific Contract

- Status: `provisional_v1.1_management`
- Paper score: `disabled_until_fresh_spectre_certification`
- Form: `bugfix`
- Family: `bugfix`
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

Repair a metastability window boundary or monotonic latency bug.

Do not satisfy this task with a generic state scaffold. The implementation
must preserve the named circuit-function behavior and expose both the
`out` waveform and the task-specific `metric` monitor.

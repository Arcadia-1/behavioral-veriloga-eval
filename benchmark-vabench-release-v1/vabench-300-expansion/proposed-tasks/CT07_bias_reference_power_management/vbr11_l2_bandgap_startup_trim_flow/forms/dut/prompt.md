# Task: bandgap_startup_trim:dut

## Release Task Contract

- Form: `dut`
- Level: `L2`
- Category: Bias Reference and Power Management
- Base function: Bandgap startup and trim convergence flow
- Domain: `voltage`
- Target artifact(s): `bandgap_startup_trim.va`
- Supplied/reference support artifact(s): `tb_bandgap_startup_trim.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## L2 Background And Claim Boundary

This Level-2 row is a behavioral composition/flow task for Bandgap startup and trim convergence flow. It should expose intermediate state, multi-stage behavior, or a closed-loop relation through the public observables below.
Stay within the listed voltage-domain/event-driven contract. Do not use transistor-level devices, current-domain loads, AC/noise analysis, S-parameters, or hidden checker logic unless the public contract explicitly lists them.
Paper-facing claims for this row are limited to the public behavior checks below; do not broaden the task into full silicon implementation, layout, device physics, or unlisted performance metrics.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `bandgap_startup_trim.va` declares module `bandgap_startup_trim` with positional ports: `in`, `clk`, `rst`, `out`, `metric`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=260n maxstep=500p
```


## Public Behavior Checks

- `bandgap_startup_trim_full_behavior`
- `startup_trim_state_near_miss_rejection`

## Output Contract

Return exactly one source artifact named `bandgap_startup_trim.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: bandgap_startup_trim:dut

## vaBench-300 v1.1 Task-Specific Contract

- Status: `provisional_v1.1_management`
- Paper score: `disabled_until_fresh_spectre_certification`
- Form: `dut`
- Family: `spec-to-va`
- Level: `L2`
- Track: `core`
- Difficulty: `D3`
- Category: Bias Reference and Power Management
- Base function target: Bandgap startup and trim convergence flow
- Domain: voltage-domain behavioral Verilog-A

This row has been rebuilt from the original v1.1 management scaffold into
a task-specific benchmark candidate. It remains outside the paper score
denominator until fresh EVAS/Spectre certification is recorded for this
rebuilt source asset.

## Current Public Interface

- Verilog-A artifact: `bandgap_startup_trim.va`
- Spectre testbench artifact: `tb_bandgap_startup_trim.scs`
- Module name: `bandgap_startup_trim`
- Positional ports: `in`, `clk`, `rst`, `out`, `metric`
- Port roles:
  - `in`: voltage-coded stimulus input.
  - `clk`: voltage-coded event clock, low=0 V and high=1 V.
  - `rst`: voltage-coded reset pulse.
  - `out`: bounded state/output monitor.
  - `metric`: derived state metric monitor.

## Task-Specific Observable Contract

- Behavior: bandgap startup and trim loop that ramps a reference toward a bounded settled target.
- Observable: out is the reference voltage monitor; metric is the startup/settle completion monitor.
- Checker: reference rises from reset to the target window and metric asserts only after settling.
- Rising `rst` clears state before the measurement window.
- Rising `clk` events drive the discrete-time behavior.
- The Spectre scaffold instantiates the DUT with instance-first AHDL syntax
  and records `time`, `in`, `clk`, `rst`, `out`, and `metric`.

## Task Goal

Implement a bandgap startup and trim convergence behavioral flow.

Do not satisfy this task with a generic state scaffold. The implementation
must preserve the named circuit-function behavior and expose both the
`out` waveform and the task-specific `metric` monitor.

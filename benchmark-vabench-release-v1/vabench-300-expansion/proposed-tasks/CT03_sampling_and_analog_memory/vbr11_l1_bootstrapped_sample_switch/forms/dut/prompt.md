# Task: bootstrapped_sample_switch:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Sampling and Analog Memory
- Base function: Bootstrapped sample switch abstraction
- Domain: `voltage`
- Target artifact(s): `bootstrapped_sample_switch.va`
- Supplied/reference support artifact(s): `tb_bootstrapped_sample_switch.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `bootstrapped_sample_switch.va` declares module `bootstrapped_sample_switch` with positional ports: `in`, `clk`, `rst`, `out`, `metric`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=260n maxstep=500p
```


## Public Behavior Checks

- `bootstrapped_sample_switch_full_behavior`
- `sample_hold_phase_near_miss_rejection`

## Output Contract

Return exactly one source artifact named `bootstrapped_sample_switch.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: bootstrapped_sample_switch:dut

## vaBench-300 v1.1 Task-Specific Contract

- Status: `provisional_v1.1_management`
- Paper score: `disabled_until_fresh_spectre_certification`
- Form: `dut`
- Family: `spec-to-va`
- Level: `L1`
- Track: `core`
- Difficulty: `D2`
- Category: Sampling and Analog Memory
- Base function target: Bootstrapped sample switch abstraction
- Domain: voltage-domain behavioral Verilog-A

This row has been rebuilt from the original v1.1 management scaffold into
a task-specific benchmark candidate. It remains outside the paper score
denominator until fresh EVAS/Spectre certification is recorded for this
rebuilt source asset.

## Current Public Interface

- Verilog-A artifact: `bootstrapped_sample_switch.va`
- Spectre testbench artifact: `tb_bootstrapped_sample_switch.scs`
- Module name: `bootstrapped_sample_switch`
- Positional ports: `in`, `clk`, `rst`, `out`, `metric`
- Port roles:
  - `in`: voltage-coded stimulus input.
  - `clk`: voltage-coded event clock, low=0 V and high=1 V.
  - `rst`: voltage-coded reset pulse.
  - `out`: bounded state/output monitor.
  - `metric`: derived state metric monitor.

## Task-Specific Observable Contract

- Behavior: sample/hold switch abstraction with clocked acquisition and bounded hold leakage.
- Observable: out holds the sampled input between acquisition events; metric reports hold quality.
- Checker: output has sample response and late-window hold-quality metric remains high.
- Rising `rst` clears state before the measurement window.
- Rising `clk` events drive the discrete-time behavior.
- The Spectre scaffold instantiates the DUT with instance-first AHDL syntax
  and records `time`, `in`, `clk`, `rst`, `out`, and `metric`.

## Task Goal

Implement a bootstrapped sample-switch abstraction.

Do not satisfy this task with a generic state scaffold. The implementation
must preserve the named circuit-function behavior and expose both the
`out` waveform and the task-specific `metric` monitor.

# Task: sigma_delta_modulator_loop:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converter Models
- Base function: First-order sigma-delta modulator loop
- Domain: `voltage`
- Target artifact(s): `sigma_delta_modulator_loop.va`
- Supplied/reference support artifact(s): `tb_sigma_delta_modulator_loop.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `sigma_delta_modulator_loop.va` declares module `sigma_delta_modulator_loop` with positional ports: `in`, `clk`, `rst`, `out`, `metric`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=260n maxstep=500p
```


## Public Behavior Checks

- `sigma_delta_modulator_loop_full_behavior`
- `integrator_feedback_boundary_near_miss_rejection`

## Output Contract

Return exactly one source artifact named `sigma_delta_modulator_loop.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: sigma_delta_modulator_loop:dut

## vaBench-300 v1.1 Task-Specific Contract

- Status: `provisional_v1.1_management`
- Paper score: `disabled_until_fresh_spectre_certification`
- Form: `dut`
- Family: `spec-to-va`
- Level: `L1`
- Track: `core`
- Difficulty: `D3`
- Category: Data Converter Models
- Base function target: First-order sigma-delta modulator loop
- Domain: voltage-domain behavioral Verilog-A

This row has been rebuilt from the original v1.1 management scaffold into
a task-specific benchmark candidate. It remains outside the paper score
denominator until fresh EVAS/Spectre certification is recorded for this
rebuilt source asset.

## Current Public Interface

- Verilog-A artifact: `sigma_delta_modulator_loop.va`
- Spectre testbench artifact: `tb_sigma_delta_modulator_loop.scs`
- Module name: `sigma_delta_modulator_loop`
- Positional ports: `in`, `clk`, `rst`, `out`, `metric`
- Port roles:
  - `in`: voltage-coded stimulus input.
  - `clk`: voltage-coded event clock, low=0 V and high=1 V.
  - `rst`: voltage-coded reset pulse.
  - `out`: bounded state/output monitor.
  - `metric`: derived state metric monitor.

## Task-Specific Observable Contract

- Behavior: first-order sigma-delta loop with clocked integrator, one-bit feedback DAC, and bit-density metric.
- Observable: out is a one-bit decision stream; metric is the running one-density over the stimulus window.
- Checker: bit stream toggles, density remains bounded, and metric tracks the one-density.
- Rising `rst` clears state before the measurement window.
- Rising `clk` events drive the discrete-time behavior.
- The Spectre scaffold instantiates the DUT with instance-first AHDL syntax
  and records `time`, `in`, `clk`, `rst`, `out`, and `metric`.

## Task Goal

Implement the DUT for a first-order sigma-delta modulator behavioral loop.

Do not satisfy this task with a generic state scaffold. The implementation
must preserve the named circuit-function behavior and expose both the
`out` waveform and the task-specific `metric` monitor.

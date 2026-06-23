# Task: sigma_delta_modulator_loop:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Data Converter Models
- Base function: First-order sigma-delta modulator loop
- Domain: `voltage`
- Target artifact(s): `tb_sigma_delta_modulator_loop.scs`
- Supplied/reference support artifact(s): `sigma_delta_modulator_loop.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.
- The supplied DUT/support Verilog-A file(s) `sigma_delta_modulator_loop.va` will be co-located with the generated testbench by the evaluation harness.
- Include it exactly with `ahdl_include "sigma_delta_modulator_loop.va"` in the generated Spectre `.scs` netlist.
- Use Spectre AHDL instance syntax with the instance name first and module name last: `XNAME (node1 node2 ...) module_name`.
- Never write module-first syntax such as `module_name instance_name (...)`; that is not the release Spectre testbench syntax.

## Public DUT Interface To Instantiate

- `sigma_delta_modulator_loop.va` declares module `sigma_delta_modulator_loop` with positional ports: `in`, `clk`, `rst`, `out`, `metric`.

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
ahdl_include "sigma_delta_modulator_loop.va"

Xdut (in clk rst out metric) sigma_delta_modulator_loop

tran tran stop=260n maxstep=500p
```

Critical syntax rules:

- Every Verilog-A DUT/support file used by the testbench must have a literal `ahdl_include "<file>.va"` line in the `.scs` artifact.
- Spectre AHDL instances use instance-first/module-last syntax: `XNAME (node1 node2 ...) module_name`.
- Do not use module-first syntax such as `module_name instance_name (...)`.
- Keep saved names as plain scalar public observables, not instance-qualified aliases.

## Public Behavior Checks

- `sigma_delta_modulator_loop_full_behavior`
- `stimulus_density_measurement_near_miss_rejection`

## Output Contract

Return exactly one source artifact named `tb_sigma_delta_modulator_loop.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: sigma_delta_modulator_loop:tb

## vaBench-300 v1.1 Task-Specific Contract

- Status: `provisional_v1.1_management`
- Paper score: `disabled_until_fresh_spectre_certification`
- Form: `tb`
- Family: `tb-generation`
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

Build a testbench that exercises bit-density and integrator stability.

Do not satisfy this task with a generic state scaffold. The implementation
must preserve the named circuit-function behavior and expose both the
`out` waveform and the task-specific `metric` monitor.

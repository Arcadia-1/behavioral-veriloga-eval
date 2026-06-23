# Task: bootstrapped_sample_switch:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Sampling and Analog Memory
- Base function: Bootstrapped sample switch abstraction
- Domain: `voltage`
- Target artifact(s): `tb_bootstrapped_sample_switch.scs`
- Supplied/reference support artifact(s): `bootstrapped_sample_switch.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.
- The supplied DUT/support Verilog-A file(s) `bootstrapped_sample_switch.va` will be co-located with the generated testbench by the evaluation harness.
- Include it exactly with `ahdl_include "bootstrapped_sample_switch.va"` in the generated Spectre `.scs` netlist.
- Use Spectre AHDL instance syntax with the instance name first and module name last: `XNAME (node1 node2 ...) module_name`.
- Never write module-first syntax such as `module_name instance_name (...)`; that is not the release Spectre testbench syntax.

## Public DUT Interface To Instantiate

- `bootstrapped_sample_switch.va` declares module `bootstrapped_sample_switch` with positional ports: `in`, `clk`, `rst`, `out`, `metric`.

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
ahdl_include "bootstrapped_sample_switch.va"

Xdut (in clk rst out metric) bootstrapped_sample_switch

tran tran stop=260n maxstep=500p
```

Critical syntax rules:

- Every Verilog-A DUT/support file used by the testbench must have a literal `ahdl_include "<file>.va"` line in the `.scs` artifact.
- Spectre AHDL instances use instance-first/module-last syntax: `XNAME (node1 node2 ...) module_name`.
- Do not use module-first syntax such as `module_name instance_name (...)`.
- Keep saved names as plain scalar public observables, not instance-qualified aliases.

## Public Behavior Checks

- `bootstrapped_sample_switch_full_behavior`
- `hold_error_measurement_near_miss_rejection`

## Output Contract

Return exactly one source artifact named `tb_bootstrapped_sample_switch.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: bootstrapped_sample_switch:tb

## vaBench-300 v1.1 Task-Specific Contract

- Status: `provisional_v1.1_management`
- Paper score: `disabled_until_fresh_spectre_certification`
- Form: `tb`
- Family: `tb-generation`
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

Build a testbench for sample/hold timing and hold error.

Do not satisfy this task with a generic state scaffold. The implementation
must preserve the named circuit-function behavior and expose both the
`out` waveform and the task-specific `metric` monitor.

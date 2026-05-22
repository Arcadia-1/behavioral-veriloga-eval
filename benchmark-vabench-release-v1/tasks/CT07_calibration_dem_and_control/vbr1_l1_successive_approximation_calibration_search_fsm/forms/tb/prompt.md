# Task: vbr1_l1_successive_approximation_calibration_search_fsm:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Successive-approximation calibration/search FSM
- Domain: `voltage`
- Target artifact(s): `tb_successive_approximation_calibration_search_fsm.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

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

## Public Behavior Checks

- `step_size_halves`
- `trim_direction_follows_error`
- `done_after_search_window`

## Output Contract

Return exactly one source artifact named `tb_successive_approximation_calibration_search_fsm.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Successive-approximation calibration/search FSM (tb-generation)

Write a Spectre transient testbench for the described behavioral Verilog-A module.

Behavioral intent:

Run a clocked successive-approximation trim search with halving step size and completion flag.

Module name: `successive_approximation_calibration_search_fsm`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module successive_approximation_calibration_search_fsm(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is a signed error stimulus around 0.45 V. out is a bounded trim/control voltage. metric is a voltage-coded status or completion observable.

Saved waveform columns:

```text
clk rst vin out metric
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

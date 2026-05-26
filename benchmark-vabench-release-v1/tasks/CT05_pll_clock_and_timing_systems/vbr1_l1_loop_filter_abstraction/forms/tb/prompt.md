# Task: vbr1_l1_loop_filter_abstraction:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: PLL Clock and Timing Systems
- Base function: Sampled loop-filter abstraction
- Domain: `voltage`
- Target artifact(s): `tb_loop_filter_abstraction.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate the target artifact: `tb_loop_filter_abstraction.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `loop_filter_abstraction.va` declares module `loop_filter_abstraction` with positional ports from the public port contract below.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=80n maxstep=0.5n
```

The release harness expects these exact public scalar observables:

```text
clk rst vin out metric
```

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- proportional_step_decays
- integral_residual_accumulates
- metric_asserts_after_valid_updates
- reset_clears_integrator
- filtered_output_bounded

## Output Contract

Return exactly these source artifacts:

- `tb_loop_filter_abstraction.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

### Sampled loop-filter abstraction (tb-generation)

Write a Spectre transient testbench for the described behavioral Verilog-A module.

Behavioral intent:

Approximate the continuous-time proportional/integral loop-filter trend with sampled voltage-domain state updates on clock edges.

Module name: `loop_filter_abstraction`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

This is a sampled/event-driven behavioral abstraction of the loop-filter control trend. It must not require current-domain charge storage, true continuous-time RC integration, or KCL/KVL solving.


Public port contract:

```verilog
module loop_filter_abstraction(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is a signed loop-error stimulus around 0.45 V. out is a bounded loop-control voltage. metric is a voltage-coded update/convergence observable.

Saved waveform columns:

```text
clk rst vin out metric
```

Public behavior checks:

- proportional_step_decays
- integral_residual_accumulates
- metric_asserts_after_valid_updates
- reset_clears_integrator
- filtered_output_bounded

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

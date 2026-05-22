# Task: vbr1_l1_higher_order_filter:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Analog Behavioral Signal Conditioning
- Base function: Higher-order filter
- Domain: `voltage`
- Target artifact(s): `higher_order_filter.va`, `tb_higher_order_filter.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `higher_order_filter.va`, `tb_higher_order_filter.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `higher_order_filter.va` declares module `higher_order_filter` with positional ports: `clk`, `rst`, `vin`, `out`, `metric`.

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

- `two_filter_states`
- `step_response_is_smoothed`
- `reset_clears_states`

## Output Contract

Return exactly these source artifacts:

- `higher_order_filter.va`
- `tb_higher_order_filter.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Higher-order filter (end-to-end)

Write both the Verilog-A behavioral module and a Spectre transient testbench.

Behavioral intent:

Approximate a second-order low-pass response with two sampled internal filter states.

Module name: `higher_order_filter`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module higher_order_filter(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. out is the bounded conditioned voltage. metric exposes the filter/settling internal response.

Saved waveform columns:

```text
clk rst vin out metric
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

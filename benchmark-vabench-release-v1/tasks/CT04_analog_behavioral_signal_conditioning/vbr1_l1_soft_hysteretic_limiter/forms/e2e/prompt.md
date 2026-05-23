# Task: vbr1_l1_soft_hysteretic_limiter:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Analog Behavioral Signal Conditioning
- Base function: Soft/hysteretic limiter
- Domain: `voltage`
- Target artifact(s): `soft_hysteretic_limiter.va`, `tb_soft_hysteretic_limiter.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `soft_hysteretic_limiter.va`, `tb_soft_hysteretic_limiter.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `soft_hysteretic_limiter.va` declares module `soft_hysteretic_limiter` with positional ports: `clk`, `rst`, `vin`, `out`, `metric`.

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

- `soft_compression`
- `hysteresis_state_memory`
- `state_metric_tracks_memory`
- `bounded_output`

## Output Contract

Return exactly these source artifacts:

- `soft_hysteretic_limiter.va`
- `tb_soft_hysteretic_limiter.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Soft/hysteretic limiter (end-to-end)

Write both the Verilog-A behavioral module and a Spectre transient testbench.

Behavioral intent:

Limit a voltage signal with soft compression and stateful hysteresis around thresholds.
The auxiliary metric reports the retained hysteresis state.

Module name: `soft_hysteretic_limiter`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module soft_hysteretic_limiter(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. out is the bounded, softly limited voltage. metric exposes the retained hysteresis state so neutral input after a high excursion differs from neutral input after a low excursion.

Saved waveform columns:

```text
clk rst vin out metric
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

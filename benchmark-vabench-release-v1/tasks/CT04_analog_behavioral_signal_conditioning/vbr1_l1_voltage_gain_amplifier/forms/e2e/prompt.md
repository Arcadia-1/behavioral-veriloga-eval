# Task: vbr1_l1_voltage_gain_amplifier:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Analog Behavioral Signal Conditioning
- Base function: Voltage gain amplifier
- Domain: `voltage`
- Target artifact(s): `voltage_gain_amplifier.va`, `tb_voltage_gain_amplifier.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `voltage_gain_amplifier.va`, `tb_voltage_gain_amplifier.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `voltage_gain_amplifier.va` declares module `voltage_gain_amplifier` with positional ports: `clk`, `rst`, `vin`, `out`, `metric`.

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

- `sampled_gain_tracks_input`
- `common_mode_offset`
- `rail_clamps`
- `saturation_metric_marks_clipping`

## Output Contract

Return exactly these source artifacts:

- `voltage_gain_amplifier.va`
- `tb_voltage_gain_amplifier.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Voltage gain amplifier (end-to-end)

Write both the Verilog-A behavioral module and a Spectre transient testbench.

Behavioral intent:

Apply a sampled voltage-domain gain with output common-mode offset and rail clamps.
The auxiliary metric reports whether the unclamped gain target hit a rail.

Module name: `voltage_gain_amplifier`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module voltage_gain_amplifier(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. out is the bounded conditioned voltage. metric exposes a saturation flag that is high when the gained target clips to either rail and low otherwise.

Saved waveform columns:

```text
clk rst vin out metric
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

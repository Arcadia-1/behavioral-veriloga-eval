# Task: vbr1_l2_amplifier_filter_chain:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Baseband Signal Conditioning
- Base function: Amplifier/filter chain
- Domain: `voltage`
- Target artifact(s): `amplifier_filter_chain.va`, `tb_amplifier_filter_chain.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `amplifier_filter_chain.va`, `tb_amplifier_filter_chain.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `amplifier_filter_chain.va` declares module `amplifier_filter_chain` with positional ports from the public port contract below.

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

- amplified_input
- filtered_output_lags_input
- metric_tracks_settling

## Output Contract

Return exactly these source artifacts:

- `amplifier_filter_chain.va`
- `tb_amplifier_filter_chain.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

### Amplifier/filter chain (end-to-end)

Write both the Verilog-A behavioral module and a Spectre transient testbench.

Behavioral intent:

Combine a gain block and low-pass filter and expose the filtered response metric.

Module name: `amplifier_filter_chain`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.


Public port contract:

```verilog
module amplifier_filter_chain(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. out is the bounded conditioned voltage. metric exposes the filter/settling internal response.

Saved waveform columns:

```text
clk rst vin out metric
```

Public behavior checks:

- amplified_input
- filtered_output_lags_input
- metric_tracks_settling

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

# Task: vbr1_l2_adc_dac_source_sweep_flow:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Stimulus and Sources
- Base function: ADC/DAC source sweep flow
- Domain: `voltage`
- Target artifact(s): `adc_dac_source_sweep_flow.va`, `tb_adc_dac_source_sweep_flow.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `adc_dac_source_sweep_flow.va`, `tb_adc_dac_source_sweep_flow.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `adc_dac_source_sweep_flow.va` declares module `adc_dac_source_sweep_flow` with positional ports: `clk`, `rst`, `vin`, `aux`, `out`, `metric`.

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
- `aux`

## Public Behavior Checks

- `code_monotonic_with_input`
- `reconstruction_follows_code`
- `saturation_at_rails`

## Output Contract

Return exactly these source artifacts:

- `adc_dac_source_sweep_flow.va`
- `tb_adc_dac_source_sweep_flow.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# ADC/DAC source sweep flow (end-to-end)

Write both the Verilog-A behavioral module and a Spectre transient testbench.

Behavioral intent:

Sweep an analog input through a small quantizer and DAC reconstruction path.

Module name: `adc_dac_source_sweep_flow`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.

Public port contract:

```verilog
module adc_dac_source_sweep_flow(clk, rst, vin, aux, out, metric);
input clk, rst, vin, aux;
output out, metric;
electrical clk, rst, vin, aux, out, metric
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is the analog stimulus. aux is a reserved analog control input. out is the reconstructed output voltage. metric is a voltage-coded public observable.

Saved waveform columns:

```text
clk rst vin out metric
```

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

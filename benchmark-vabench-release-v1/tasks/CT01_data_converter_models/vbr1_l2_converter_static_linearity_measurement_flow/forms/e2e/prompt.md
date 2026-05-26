# Task: vbr1_l2_converter_static_linearity_measurement_flow:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Data Converter Models
- Base function: Converter static linearity measurement flow
- Domain: `voltage`
- Target artifact(s): `converter_static_linearity_measurement_flow.va`, `tb_converter_static_linearity_measurement_flow.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `converter_static_linearity_measurement_flow.va`, `tb_converter_static_linearity_measurement_flow.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `converter_static_linearity_measurement_flow.va` declares module `converter_static_linearity_measurement_flow` with positional ports: `clk`, `rst`, `vin`, `code`, `recon`, `dnl`, `inl`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=96n maxstep=250p
```

The release harness expects these exact public scalar observables:

- `clk`
- `rst`
- `vin`
- `code`
- `recon`
- `dnl`
- `inl`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `clk`
- `rst`
- `vin`

## Public Behavior Checks

- `ramp_code_coverage`
- `monotonic_reconstruction`
- `nonuniform_dnl_metric`
- `inl_metric_matches_reconstruction_error`
- `dnl_metric_matches_step_error`

## Output Contract

Return exactly these source artifacts:

- `converter_static_linearity_measurement_flow.va`
- `tb_converter_static_linearity_measurement_flow.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Converter static linearity measurement flow (end-to-end)

Build a voltage-domain static-linearity characterization flow for a 4-bit converter pair.

The circuit samples an input ramp, quantizes it to a 4-bit code, reconstructs a deliberately
non-ideal DAC voltage, and uses a lightweight measurement stage to derive DNL/INL-like
metric voltages from the observed reconstruction. This is a converter measurement flow:
the checker observes code coverage, monotonic reconstruction, non-uniform code steps, and
metric consistency against the measured code/reconstruction history.

Public port contract:

```verilog
module converter_static_linearity_measurement_flow(clk, rst, vin, code, recon, dnl, inl);
input clk, rst, vin;
output code, recon, dnl, inl;
electrical clk, rst, vin, code, recon, dnl, inl;
```

Signal contract:

All logic controls are voltage-coded, low=0 V and high=0.9 V with threshold 0.45 V. The design remains pure voltage-domain behavioral Verilog-A: no current contributions, transistor devices, AC/noise analysis, or KCL/KVL solving assumptions.

Saved waveform columns:

```text
clk rst vin code recon dnl inl
```

Public transient contract:

```spectre
tran tran stop=96n maxstep=0.25n
```

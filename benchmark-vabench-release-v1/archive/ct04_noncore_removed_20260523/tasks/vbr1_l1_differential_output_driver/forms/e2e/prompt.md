# Task: vbr1_l1_differential_output_driver:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Differential output driver
- Domain: `voltage`
- Target artifact(s): `differential_voltage_output_ref.va`, `tb_differential_voltage_output_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `differential_voltage_output_ref.va`, `tb_differential_voltage_output_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `differential_voltage_output_ref.va` declares module `differential_voltage_output_ref` with positional ports: `VDD`, `VSS`, `din`, `en`, `outp`, `outn`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=100n maxstep=100p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `din`
- `en`
- `outp`
- `outn`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`
- `din`
- `en`

## Public Behavior Checks

- `differential_output_driver`

## Output Contract

Return exactly these source artifacts:

- `differential_voltage_output_ref.va`
- `tb_differential_voltage_output_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `differential_voltage_output_ref`.

# Task: differential_voltage_output_smoke

## Objective

Write a Verilog-A differential output driver with digital-like input and enable controls. The task is a driver model, not a free-running voltage source.

## Specification

- **Module name**: `differential_voltage_output_ref`
- **Ports**: `VDD`, `VSS`, `din`, `en`, `outp`, `outn` - all `electrical`
- **Behavior**:
  - Use `vcm=0.45 V`, `vod=0.4 V`, and `vth=0.45 V` by default.
  - When `en` is LOW, drive both outputs to the common-mode level.
  - When `en` is HIGH and `din` is LOW, drive `outp-outn` negative.
  - When `en` is HIGH and `din` is HIGH, drive `outp-outn` positive.
  - Keep both outputs bounded between `VSS` and `VDD` and use finite `transition(...)` edges.
- **Expected observable behavior**:
  - Disabled windows have near-zero differential output.
  - Enabled low-input windows have negative differential output.
  - Enabled high-input windows have positive differential output.
  - The output common-mode remains near `vcm`.

## Constraints

- Use `transition(...)` for the driven outputs.
- Pure voltage-domain only.
- No `I() <+`, `ddt()`, or `idt()`.

Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `din`: input electrical
- `en`: input electrical
- `outp`: output electrical
- `outn`: output electrical

## Output Contract (MANDATORY)

- Return exactly two fenced code blocks:
  - first block: Verilog-A DUT (` ```verilog-a ... ``` `)
  - second block: Spectre testbench (` ```spectre ... ``` `)
- The Spectre testbench must include the DUT with `ahdl_include "<module>.va"`.
- Use a single `tran` analysis and include the required `save` signals for checker evaluation.

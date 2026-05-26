# Task: vbr1_l1_differential_output_driver:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Differential output driver
- Domain: `voltage`
- Target artifact(s): `tb_differential_voltage_output_ref.scs`
- Supplied/reference support artifact(s): `differential_voltage_output_ref.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

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

- `transient_analysis_present`
- `public_observables_saved`
- `dut_or_system_instantiated`

## Output Contract

Return exactly one source artifact named `tb_differential_voltage_output_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Differential output driver TB Companion

Write a Spectre transient testbench for this behavioral release task.

This task form is materialized from the already source-controlled `e2e`
release gold for `Differential output driver`. It exists to make the public
benchmark split complete without inventing a new circuit kernel or a fake
bugfix.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the checker
- include or instantiate the behavioral module under test
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

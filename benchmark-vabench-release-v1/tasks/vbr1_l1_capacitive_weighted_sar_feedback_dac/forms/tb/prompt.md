# Task: vbr1_l1_capacitive_weighted_sar_feedback_dac:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Data Converters
- Base function: Capacitive/weighted SAR feedback DAC
- Domain: `voltage`
- Target artifact(s): `tb_cdac_cal_ref.scs`
- Supplied/reference support artifact(s): `cdac_cal.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `cdac_cal.va` declares module `cdac_cal` with positional ports: `VDD`, `VSS`, `CLK`, `D9`, `D8`, `D7`, `D6`, `D5`, `D4`, `D3`, `D2`, `D1`, `D0`, `CAL0`, `CAL1`, `VDAC_P`, `VDAC_N`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=68n maxstep=20p
```

The release harness expects these exact public scalar observables:

- `CLK`
- `CAL0`
- `CAL1`
- `VDAC_P`
- `VDAC_N`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`
- `CLK`
- `D0`
- `D1`
- `D2`
- `D3`
- `D4`
- `D5`
- `D6`
- `D7`
- `D8`
- `D9`
- `CAL0`
- `CAL1`

## Public Behavior Checks

- `transient_analysis_present`
- `public_observables_saved`
- `dut_or_system_instantiated`

## Output Contract

Return exactly one source artifact named `tb_cdac_cal_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Capacitive/weighted SAR feedback DAC TB Companion

Write a Spectre transient testbench for this behavioral release task.

This task form is materialized from the already source-controlled `dut`
release gold for `Capacitive/weighted SAR feedback DAC`. It exists to make the public
benchmark split complete without inventing a new circuit kernel or a fake
bugfix.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the checker
- include or instantiate the behavioral module under test
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

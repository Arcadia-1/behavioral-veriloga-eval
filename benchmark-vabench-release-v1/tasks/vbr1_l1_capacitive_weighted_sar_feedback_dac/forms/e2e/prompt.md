# Task: vbr1_l1_capacitive_weighted_sar_feedback_dac:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Data Converters
- Base function: Capacitive/weighted SAR feedback DAC
- Domain: `voltage`
- Target artifact(s): `cdac_cal.va`, `tb_cdac_cal_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `cdac_cal.va`, `tb_cdac_cal_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

- `behavioral_module_present`
- `transient_analysis_present`
- `public_observables_saved`

## Output Contract

Return exactly these source artifacts:

- `cdac_cal.va`
- `tb_cdac_cal_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Capacitive/weighted SAR feedback DAC E2E Companion

Write both the Verilog-A behavioral module and a Spectre transient testbench.

This task form is materialized from the already source-controlled `dut`
release gold for `Capacitive/weighted SAR feedback DAC`. It exists to make the public
benchmark split complete without inventing a new circuit kernel or a fake
bugfix.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include the behavioral Verilog-A module
- include a transient `tran` analysis
- save the public observables needed by the checker
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

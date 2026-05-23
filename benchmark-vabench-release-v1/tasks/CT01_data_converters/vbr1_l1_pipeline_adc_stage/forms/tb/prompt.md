# Task: vbr1_l1_pipeline_adc_stage:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Data Converters
- Base function: Pipeline ADC MDAC stage
- Domain: `voltage`
- Target artifact(s): `tb_pipeline_stage_ref.scs`
- Supplied/reference support artifact(s): `pipeline_stage.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `pipeline_stage.va` declares module `pipeline_stage` with positional ports: `VDD`, `VSS`, `PHI1`, `PHI2`, `VIN`, `VREF`, `VRES`, `D1`, `D0`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=300n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `phi1`
- `phi2`
- `vin`
- `vres`
- `d1`
- `d0`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `vref`
- `phi1`
- `phi2`
- `vin`

## Public Behavior Checks

- `upper_middle_lower_regions_exercised`
- `sub_adc_decisions_match_thresholds`
- `residue_follows_gain_two_mdac_formula`
- `residue_output_bounded`

## Output Contract

Return exactly one source artifact named `tb_pipeline_stage_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Spectre transient testbench for `pipeline_stage`.

Public requirements:

- use a 0.9 V supply, 0 V reference, and 0.9 V `VREF`
- drive non-overlapping `PHI1` and `PHI2` clocks
- step `VIN` through upper, middle, and lower MDAC decision regions:
  above `Vcm + VREF/4`, near `Vcm`, and below `Vcm - VREF/4`
- instantiate `pipeline_stage` by positional ports
- save exactly `phi1`, `phi2`, `vin`, `vres`, `d1`, and `d0`
- include a transient `tran` analysis
- avoid transistor-level devices, AC/noise analysis, and current-domain solver assumptions

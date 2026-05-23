# Task: vbr1_l1_pipeline_adc_stage:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Data Converters
- Base function: Pipeline ADC MDAC stage
- Domain: `voltage`
- Target artifact(s): `pipeline_stage.va`, `tb_pipeline_stage_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `pipeline_stage.va`, `tb_pipeline_stage_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

Return exactly these source artifacts:

- `pipeline_stage.va`
- `tb_pipeline_stage_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Create a pure voltage-domain 1.5-bit pipeline ADC MDAC stage and matching
Spectre testbench. The DUT samples `VIN` on `PHI1`, makes a sub-ADC decision on
`PHI2`, drives `D1/D0`, and outputs the gain-of-2 residue for the next stage.

Public behavior:

- upper region: `VIN - Vcm > VREF/4`, drive `D1=1`, `D0=0`,
  `VRES = Vcm + 2*(VIN - Vcm) - VREF/2`
- lower region: `VIN - Vcm < -VREF/4`, drive `D1=0`, `D0=0`,
  `VRES = Vcm + 2*(VIN - Vcm) + VREF/2`
- middle region: drive `D1=0`, `D0=1`,
  `VRES = Vcm + 2*(VIN - Vcm)`

The testbench must use non-overlapping `PHI1`/`PHI2`, exercise all three
regions, save `phi1`, `phi2`, `vin`, `vres`, `d1`, and `d0`, and keep all
behavior pure voltage-domain with `transition(...)`.

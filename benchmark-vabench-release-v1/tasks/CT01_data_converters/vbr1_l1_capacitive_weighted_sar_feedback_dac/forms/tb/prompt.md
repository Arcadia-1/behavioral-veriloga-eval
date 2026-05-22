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

Required public stimulus pattern for this benchmark form:

- Drive `VDD` at 0.9 V and `VSS` at 0 V.
- Drive `CLK` as a 0-to-0.9 V pulse with delay 1n, rise/fall 20p, width 1n,
  and period 4n.
- Starting at 2n and then every 4n, drive `D9`...`D0` through this sparse
  10-bit code sequence before the next `CLK` rising edge:
  `0, 1, 2, 3, 7, 15, 16, 32, 64, 128, 256, 512, 255, 511, 767, 1023`.
- In the same code windows, drive `CAL0`/`CAL1` through calibration codes
  `0, 1, 2, 3` repeatedly, where `CAL0` is the LSB and `CAL1` is the MSB.
- Use deterministic voltage sources such as `type=pwl` with logic high 0.9 V
  and logic low 0 V for the data and calibration inputs.

## Public Behavior Checks

- `transient_analysis_present`
- `public_observables_saved`
- `dut_or_system_instantiated`
- `sparse_10bit_code_stimulus_exercised`
- `calibration_stimulus_exercised`
- `differential_outputs_observable`

## Output Contract

Return exactly one source artifact named `tb_cdac_cal_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Capacitive/weighted SAR feedback DAC TB Companion

Write a Spectre transient testbench for the supplied `cdac_cal` behavioral DUT.

Domain: pure voltage-domain behavioral Verilog-A.

Public testbench requirements:

- include or instantiate the supplied behavioral module under test using the
  public positional port order
- include the public transient `tran` analysis
- use the required public stimulus pattern above so both binary code changes and
  calibration-bit changes are exercised across low, mid, and high 10-bit codes
- save the exact public scalar observables listed above
- avoid transistor-level devices, AC/noise analysis, and current-domain solver
  assumptions

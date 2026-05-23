# Task: vbr1_l2_gain_extraction_convergence_measurement_flow:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Measurement and Testbench Instrumentation
- Base function: Gain extraction/convergence measurement flow
- Domain: `voltage`
- Target artifact(s): `tb_gain_extraction_ref.scs`
- Supplied/reference support artifact(s): `dither_adder.va`, `gain_amp_fixed.va`, `lfsr.va`, `vin_src.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `dither_adder.va` declares module `dither_adder` with positional ports: `VRES_P`, `VRES_N`, `DPN`, `VOUT_P`, `VOUT_N`.
- `gain_amp_fixed.va` declares module `gain_amp_fixed` with positional ports: `VIN_P`, `VIN_N`, `VOUT_P`, `VOUT_N`.
- `lfsr.va` declares module `lfsr` with positional ports: `DPN`, `VDD`, `VSS`, `CLK`, `EN`, `RSTB`.
- `vin_src.va` declares module `vin_src` with positional ports: `CLK`, `RST_N`, `VOUT_P`, `VOUT_N`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=200u maxstep=8n
```

The release harness expects these exact public scalar observables:

- `vinp`
- `vinn`
- `vamp_p`
- `vamp_n`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clk`
- `rst_n`
- `en`

## Public Behavior Checks

- `gain_amplification_present`
- `differential_gain_above_threshold`

## Output Contract

Return exactly one source artifact named `tb_gain_extraction_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Gain extraction/convergence measurement flow Testbench Companion

Write a Spectre transient testbench for the `Gain extraction/convergence measurement flow` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the public behavior checks
- include or instantiate the Verilog-A behavioral module under test
- satisfy the named behavior checks using only public waveforms and side outputs
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

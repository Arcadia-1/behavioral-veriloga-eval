# Task: vbr1_l2_weighted_sar_adc_dac_loop:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Data Converters
- Base function: Weighted SAR ADC/DAC loop
- Domain: `voltage`
- Target artifact(s): `tb_sar_adc_dac_weighted_8b_ref.scs`
- Supplied/reference support artifact(s): `dac_weighted_8b.va`, `sar_adc_weighted_8b.va`, `sh_ideal.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `dac_weighted_8b.va` declares module `dac_weighted_8b` with positional ports: `DIN`, `VOUT`.
- `sar_adc_weighted_8b.va` declares module `sar_adc_weighted_8b` with positional ports: `VIN`, `CLKS`, `RST_N`, `DOUT`.
- `sh_ideal.va` declares module `sh_ideal` with positional ports: `vin`, `clk`, `vdd`, `vss`, `rst_n`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=10u maxstep=5n
```

The release harness expects these exact public scalar observables:

- `vin`
- `vin_sh`
- `clks`
- `rst_n`
- `vout`
- `dout_7`
- `dout_6`
- `dout_5`
- `dout_4`
- `dout_3`
- `dout_2`
- `dout_1`
- `dout_0`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clks`
- `rst_n`
- `vin`

## Public Behavior Checks

- `transient_analysis_present`
- `public_observables_saved`
- `dut_or_system_instantiated`

## Output Contract

Return exactly one source artifact named `tb_sar_adc_dac_weighted_8b_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Weighted SAR ADC/DAC loop Testbench Companion

Write a Spectre transient testbench for the `Weighted SAR ADC/DAC loop` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the checker
- include or instantiate the Verilog-A behavioral module under test
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

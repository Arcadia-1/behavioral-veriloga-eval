# Task: vbr1_l2_flash_adc_mini_array:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Data Converter Models
- Base function: Flash ADC mini-array
- Domain: `voltage`
- Target artifact(s): `tb_flash_adc_3b_ref.scs`
- Supplied/reference support artifact(s): `flash_adc_3b.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `flash_adc_3b.va` declares module `flash_adc_3b` with positional ports: `VDD`, `VSS`, `VIN`, `CLK`, `CMP0`, `CMP1`, `CMP2`, `CMP3`, `CMP4`, `CMP5`, `CMP6`, `DOUT2`, `DOUT1`, `DOUT0`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=86n maxstep=200p
```

The release harness expects these exact public scalar observables:

- `vin`
- `clk`
- `cmp0`
- `cmp1`
- `cmp2`
- `cmp3`
- `cmp4`
- `cmp5`
- `cmp6`
- `dout2`
- `dout1`
- `dout0`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `vin`
- `clk`

## Public Behavior Checks

- `all_8_flash_codes_present`
- `comparator_threshold_ladder_matches_vin_bins`
- `comparator_outputs_form_thermometer_prefix`
- `binary_code_matches_comparator_count`

## Output Contract

Return exactly one source artifact named `tb_flash_adc_3b_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Flash ADC mini-array Testbench Companion

Write a Spectre transient testbench for a 3-bit flash ADC mini-array. The
supplied DUT exposes seven comparator decisions as a thermometer vector and
encodes that vector into a 3-bit binary output after clocked sampling.

Public requirements:

- use a 0.9 V supply and 0 V reference
- drive `vin` through the midpoint of each of the 8 quantization bins, using
  stable windows before each clock edge
- drive `clk` so the checker can sample one stable conversion for every code
  from `0` through `7`
- instantiate `flash_adc_3b` by positional ports
- save exactly these scalar names: `vin`, `clk`, `cmp0`, `cmp1`, `cmp2`,
  `cmp3`, `cmp4`, `cmp5`, `cmp6`, `dout2`, `dout1`, `dout0`
- include a transient `tran` analysis
- avoid transistor-level devices, AC/noise analysis, and current-domain solver assumptions

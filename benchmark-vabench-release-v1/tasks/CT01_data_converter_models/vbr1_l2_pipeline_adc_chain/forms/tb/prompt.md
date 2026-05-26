# Task: vbr1_l2_pipeline_adc_chain:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Data Converter Models
- Base function: Pipeline ADC residue chain
- Domain: `voltage`
- Target artifact(s): `tb_pipeline_adc_chain_4b_ref.scs`
- Supplied/reference support artifact(s): `pipeline_adc_chain_4b.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `pipeline_adc_chain_4b.va` declares module `pipeline_adc_chain_4b` with positional ports: `VDD`, `VSS`, `VIN`, `CLK`, `RES1`, `RES2`, `S1B1`, `S1B0`, `S2B1`, `S2B0`, `DOUT3`, `DOUT2`, `DOUT1`, `DOUT0`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=170n maxstep=200p
```

The release harness expects these exact public scalar observables:

- `vin`
- `clk`
- `res1`
- `res2`
- `s1b1`
- `s1b0`
- `s2b1`
- `s2b0`
- `dout3`
- `dout2`
- `dout1`
- `dout0`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clk`
- `vin`

## Public Behavior Checks

- `all_16_pipeline_codes_present`
- `stage1_residue_matches_coarse_decision`
- `stage2_residue_matches_backend_decision`
- `final_code_matches_stage_concatenation`
- `final_code_monotonic_with_vin`

## Output Contract

Return exactly one source artifact named `tb_pipeline_adc_chain_4b_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Pipeline ADC residue chain Testbench Companion

Write a Spectre transient testbench for a pure voltage-domain compact two-stage
4-bit pipeline ADC chain. The supplied DUT performs a 2-bit coarse
quantization, outputs the first residue, performs a 2-bit backend quantization,
and drives a final 4-bit code for the same sampled input. This is a
single-sample behavioral residue chain, not a latency/correction benchmark.

Public requirements:

- use a 0.9 V supply
- drive `vin` through representative points in all 16 final 4-bit code bins
- alternate lower-half and upper-half points inside adjacent bins so the
  residue path is exercised, not only the final code output
- drive `clk` so every input point is stable before a rising clock edge
- instantiate `pipeline_adc_chain_4b` by positional ports
- save exactly these scalar names: `vin`, `clk`, `res1`, `res2`, `s1b1`,
  `s1b0`, `s2b1`, `s2b0`, `dout3`, `dout2`, `dout1`, `dout0`
- include a transient `tran` analysis
- avoid transistor-level devices, AC/noise analysis, and current-domain solver assumptions

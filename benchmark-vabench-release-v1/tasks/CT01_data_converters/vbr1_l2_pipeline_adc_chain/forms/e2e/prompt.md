# Task: vbr1_l2_pipeline_adc_chain:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Data Converters
- Base function: Pipeline ADC chain
- Domain: `voltage`
- Target artifact(s): `pipeline_adc_chain_4b.va`, `tb_pipeline_adc_chain_4b_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `pipeline_adc_chain_4b.va`, `tb_pipeline_adc_chain_4b_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

Return exactly these source artifacts:

- `pipeline_adc_chain_4b.va`
- `tb_pipeline_adc_chain_4b_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: pipeline_adc_chain_e2e

Create a pure voltage-domain two-stage 4-bit pipeline ADC chain and a matching
Spectre transient testbench. The model should represent a composed converter
flow, not a single isolated MDAC stage.

## DUT Contract

- Module name: `pipeline_adc_chain_4b`
- Ports, all `electrical`, exactly in this order: `VDD`, `VSS`, `VIN`, `CLK`,
  `RES1`, `RES2`, `S1B1`, `S1B0`, `S2B1`, `S2B0`, `DOUT3`, `DOUT2`,
  `DOUT1`, `DOUT0`
- Parameters:
  - `vrefp` real, default `0.9`
  - `vrefn` real, default `0.0`
  - `vth` real, default `0.45`
  - `tedge` real, default `100p`
- Behavior:
  - On each rising `clk` edge, sample `vin`.
  - Stage 1 performs a 2-bit coarse quantization over `vrefn..vrefp`.
  - Stage 1 drives `s1b1:s1b0` and computes a residue:
    `res1 = midscale + 4*(vin_sample - stage1_bin_center)`, clipped to the
    reference range.
  - Stage 2 performs a 2-bit backend quantization of `res1`.
  - Stage 2 drives `s2b1:s2b0` and computes `res2` with the same bin-center
    residue equation.
  - The final code is the concatenation of stage 1 and stage 2 decisions:
    `dout3:dout2:dout1:dout0 = {s1b1, s1b0, s2b1, s2b0}`.
  - Use `@(cross(V(clk) - vth, +1))` and `transition(...)`.
  - Keep the implementation behavioral and voltage-domain only.

## Testbench Contract

- Use a 0.9 V supply.
- Drive `vin` through representative points in all 16 final 4-bit code bins.
- Alternate lower-half and upper-half points inside adjacent bins so the
  residue path is exercised, not only the final code output.
- Drive `clk` so every input point is stable before a rising clock edge.
- Instantiate the DUT by positional ports.
- Save exactly these scalar names: `vin`, `clk`, `res1`, `res2`, `s1b1`,
  `s1b0`, `s2b1`, `s2b0`, `dout3`, `dout2`, `dout1`, `dout0`.
- Include a transient `tran` analysis.

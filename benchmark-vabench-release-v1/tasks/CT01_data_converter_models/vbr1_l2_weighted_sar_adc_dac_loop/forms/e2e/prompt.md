# Task: vbr1_l2_weighted_sar_adc_dac_loop:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Data Converter Models
- Base function: Weighted SAR ADC/DAC loop
- Domain: `voltage`
- Target artifact(s): `dac_weighted_8b.va`, `sar_adc_weighted_8b.va`, `sh_ideal.va`, `tb_sar_adc_dac_weighted_8b_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `dac_weighted_8b.va`, `sar_adc_weighted_8b.va`, `sh_ideal.va`, `tb_sar_adc_dac_weighted_8b_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

- `sar_adc_code_range_sufficient`
- `sar_adc_unique_code_count`
- `sar_code_matches_sampled_input`
- `dac_output_matches_weighted_code`
- `code_monotonic_with_sampled_input`
- `dac_output_in_range`

## Output Contract

Return exactly these source artifacts:

- `dac_weighted_8b.va`
- `sar_adc_weighted_8b.va`
- `sh_ideal.va`
- `tb_sar_adc_dac_weighted_8b_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a voltage-domain 8-bit SAR ADC, matching weighted DAC, sample/hold helper, and one voltage-domain Spectre transient testbench.

# Task: sar_adc_dac_weighted_8b_smoke

## Objective

Create a compact weighted SAR ADC/DAC round-trip system. The ADC samples a full-swing sine input,
uses an MSB-first weighted successive-approximation final-code update for each sample, the matching
weighted DAC converts the code back to an analog output, and the checker verifies code coverage,
sample-to-code consistency, DAC reconstruction from the code, and output range.

## Required Verilog-A Modules

Return these Verilog-A modules:

1. `sar_adc_weighted_8b`
   - Ports, all `electrical`, exactly in this order:
     - `vin`, `clks`, `rst_n`, `dout[7:0]`
   - On each conversion update after reset:
     - sample or use the held input voltage for the conversion decision
     - start from zero code and test weights MSB to LSB: 128, 64, 32, 16, 8, 4, 2, 1
     - keep a tentative bit when the partial weighted DAC level does not exceed the sampled input
     - output the final 8-bit code clipped to `[0, 255]`
   - `dout_7` is MSB and `dout_0` is LSB in the scalar testbench connection.
2. `dac_weighted_8b`
   - Ports, all `electrical`, exactly in this order:
     - `din[7:0]`, `vout`
   - Output:
     - `vout = weighted_code / 255 * vdd`
3. `sh_ideal`
   - Ports, all `electrical`, exactly in this order:
     - `vin`, `clks`, `vdd`, `vss`, `rst_n`, `vin_sh`
   - Tracks or samples `vin` so the checker can observe the sampled input as `vin_sh`.

## Behavioral Contract

- Use pure voltage-domain Verilog-A only.
- Use `@(cross(V(clks) - vth, +1))` for clocked updates.
- Use `transition(...)` for all driven outputs.
- Output HIGH should use `vdd`; output LOW should use `0`.
- The ADC code range should cover most of `[0, 255]` under the testbench sine input.
- The final output code should be monotonic with the sampled input voltage across the sine sweep.
- `vout` must stay within `[0, vdd]` and match `weighted_code / 255 * vdd`.

## Testbench Contract

- Use a 0.9 V supply and 0 V reference.
- Drive `clks` with a 50 MHz-class sampling clock.
- Use active-low `rst_n` and release reset early enough to leave many post-reset samples.
- Drive `vin` with a full-swing sine input around mid-supply so the sampled input covers most ADC codes.
- Instantiate `sar_adc_weighted_8b`, `dac_weighted_8b`, and `sh_ideal` by positional scalar ports.
- Save these exact scalar names:
  - `vin`, `vin_sh`, `clks`, `rst_n`, `vout`
  - `dout_7`, `dout_6`, `dout_5`, `dout_4`, `dout_3`, `dout_2`, `dout_1`, `dout_0`

## Expected Checker-Visible Behavior

- Many distinct post-reset output codes should appear.
- Code range should span near the endpoints of the 8-bit range.
- Decoded output code should match the sampled input within quantization tolerance.
- `vout` should follow the code-derived DAC level and remain within the supply range.

# Task: vbr1_l2_flash_adc_mini_array:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Data Converters
- Base function: Flash ADC mini-array
- Domain: `voltage`
- Target artifact(s): `flash_adc_3b.va`, `tb_flash_adc_3b_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `flash_adc_3b.va`, `tb_flash_adc_3b_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

Return exactly these source artifacts:

- `flash_adc_3b.va`
- `tb_flash_adc_3b_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: flash_adc_mini_array_e2e

Create a pure voltage-domain 3-bit flash ADC mini-array. The DUT must expose
the seven comparator decisions as a thermometer vector and encode that vector
into a 3-bit binary output after clocked sampling.

## DUT Contract

- Module name: `flash_adc_3b`
- Ports, all `electrical`, exactly in this order: `vdd`, `vss`, `vin`, `clk`, `cmp0`, `cmp1`, `cmp2`, `cmp3`, `cmp4`, `cmp5`, `cmp6`, `dout2`, `dout1`, `dout0`
- Parameters:
  - `vrefp` real, default `0.9`
  - `vrefn` real, default `0.0`
  - `vth` real, default `0.45`
  - `tedge` real, default `100p`
- Behavior:
  - Full-scale range is `vrefn` to `vrefp`, divided into 8 equal bins.
  - On each rising `clk` edge, compare `V(vin)` against the seven thresholds
    `vrefn + k*(vrefp-vrefn)/8` for `k=1..7`.
  - Drive `cmp0` through `cmp6` as the latched threshold-comparator decisions,
    where `cmp0` is the 1-LSB threshold and `cmp6` is the 7-LSB threshold.
  - The comparator outputs must form a thermometer prefix: higher thresholds
    cannot be high unless all lower thresholds are high.
  - Encode the number of high comparator outputs into `dout2:dout1:dout0`,
    with `dout2` as MSB and `dout0` as LSB.
  - Output HIGH should be `V(vdd)` and output LOW should be `V(vss)`.
  - Use `@(cross(V(clk) - vth, +1))` and `transition(...)`.

## Testbench Contract

- Use a 0.9 V supply and 0 V reference.
- Drive `vin` through the midpoint of each of the 8 quantization bins, using
  stable windows before each clock edge.
- Drive `clk` so the checker can sample one stable conversion for every code
  from `0` through `7`.
- Instantiate the DUT by positional ports.
- Save these exact scalar names: `vin`, `clk`, `cmp0`, `cmp1`, `cmp2`, `cmp3`, `cmp4`, `cmp5`, `cmp6`, `dout2`, `dout1`, `dout0`.
- Include the generated DUT file `flash_adc_3b.va`.

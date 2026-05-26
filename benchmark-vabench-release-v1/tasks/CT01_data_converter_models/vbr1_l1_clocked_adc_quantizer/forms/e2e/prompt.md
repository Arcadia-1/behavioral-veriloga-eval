# Task: vbr1_l1_clocked_adc_quantizer:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Data Converter Models
- Base function: Clocked ADC quantizer
- Domain: `voltage`
- Target artifact(s): `flash_adc_3b.va`, `tb_flash_adc_3b_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `flash_adc_3b.va`, `tb_flash_adc_3b_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `flash_adc_3b.va` declares module `flash_adc_3b` with positional ports: `VDD`, `VSS`, `VIN`, `CLK`, `DOUT2`, `DOUT1`, `DOUT0`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=820n maxstep=2n
```

The release harness expects these exact public scalar observables:

- `vin`
- `clk`
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

- `flash_adc_all_8_codes_present`
- `flash_adc_monotonic_with_ramp`

## Output Contract

Return exactly these source artifacts:

- `flash_adc_3b.va`
- `tb_flash_adc_3b_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `flash_adc_3b` and one minimal voltage-domain Spectre transient testbench.

# Task: flash_adc_3b_smoke

## Objective

Create a pure voltage-domain 3-bit flash ADC behavioral model. The testbench must sweep the input
across the full reference range and produce all 8 output codes after clocked sampling.

## DUT Contract

- Module name: `flash_adc_3b`
- Ports, all `electrical`, exactly in this order: `vdd`, `vss`, `vin`, `clk`, `dout2`, `dout1`, `dout0`
- Parameters:
  - `vrefp` real, default `0.9`
  - `vrefn` real, default `0.0`
  - `vth` real, default `0.45`
  - `tedge` real, default `100p`
- Behavior:
  - On each rising `clk` edge, compute a 3-bit code from `V(vin)`.
  - Full-scale range is `vrefn` to `vrefp`, divided into 8 equal bins.
  - Clamp the code to `[0, 7]`.
  - Drive `dout2` as MSB, `dout1`, and `dout0` as LSB.
  - Output HIGH should be `V(vdd)` and output LOW should be `V(vss)`.
  - Use `@(cross(V(clk) - vth, +1))` and `transition(...)`.

## Testbench Contract

- Use a 0.9 V supply and 0 V reference.
- Drive `vin` with a monotonic full-scale sweep from near `0` to near `0.9 V` within the final validation window.
- Drive `clk` with a pulse clock fast enough to sample all 8 ADC codes during the input sweep.
- Instantiate the DUT by positional ports.
- Save these exact scalar names: `vin`, `clk`, `dout2`, `dout1`, `dout0`.
- Include the generated DUT file `flash_adc_3b.va`.

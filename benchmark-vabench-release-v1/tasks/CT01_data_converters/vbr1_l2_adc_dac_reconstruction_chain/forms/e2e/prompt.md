# Task: vbr1_l2_adc_dac_reconstruction_chain:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Data Converters
- Base function: ADC/DAC reconstruction chain
- Domain: `voltage`
- Target artifact(s): `adc_ideal_4b.va`, `adc_ideal_4b_ref.va`, `dac_ideal_4b.va`, `dac_ideal_4b_ref.va`, `tb_adc_dac_ideal_4b_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `adc_ideal_4b.va`, `adc_ideal_4b_ref.va`, `dac_ideal_4b.va`, `dac_ideal_4b_ref.va`, `tb_adc_dac_ideal_4b_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `adc_ideal_4b.va` declares module `adc_ideal_4b` with positional ports: `vin`, `clk`, `vdd`, `vss`, `rst_n`, `dout`.
- `adc_ideal_4b_ref.va` declares module `adc_ideal_4b` with positional ports: `vin`, `clk`, `vdd`, `vss`, `rst_n`, `dout`.
- `dac_ideal_4b.va` declares module `dac_ideal_4b` with positional ports: `din`, `vdd`, `vss`, `rst_n`, `vout`.
- `dac_ideal_4b_ref.va` declares module `dac_ideal_4b` with positional ports: `din`, `vdd`, `vss`, `rst_n`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=50n maxstep=100p
```

The release harness expects these exact public scalar observables:

- `vin`
- `clk`
- `rst_n`
- `vout`
- `dout_3`
- `dout_2`
- `dout_1`
- `dout_0`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clk`
- `rst_n`
- `vin`

## Public Behavior Checks

- `adc_covers_full_code_range`
- `dac_output_in_range`
- `quantization_error_within_one_lsb`

## Output Contract

Return exactly these source artifacts:

- `adc_ideal_4b.va`
- `adc_ideal_4b_ref.va`
- `dac_ideal_4b.va`
- `dac_ideal_4b_ref.va`
- `tb_adc_dac_ideal_4b_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write Verilog-A modules named `adc_ideal_4b` and `dac_ideal_4b`.

Create a voltage-domain ideal 4-bit ADC and 4-bit DAC pair in Verilog-A,
chain them for an ADC→DAC round-trip, then produce a minimal EVAS-compatible
Spectre testbench and run a smoke simulation.

Behavioral intent (ADC):

- inputs: `vin` (analog), `clk`, `vdd`, `vss`, `rst_n`
- outputs: 4-bit digital code `dout[3:0]`
- samples `vin` on each rising edge of `clk` (active-low reset holds code at 0)
- quantization: truncation-style, `code = floor(vin / vstep)`, clipped to [0, 15]
- `vstep = (vdd - vss) / 16`

Behavioral intent (DAC):

- inputs: 4-bit code `din[3:0]`, `vdd`, `vss`, `rst_n`
- output: `vout` (analog)
- combinational: `vout = code / 16 * vdd`

Implementation constraints:

- pure voltage-domain Verilog-A only
- EVAS-compatible syntax
- use `@(cross(...))` for clock edge detection in the ADC
- use `transition(...)` to drive digital and analog outputs
- `vin`, `clk`, `vout`, and all `dout` bits must appear in the waveform CSV

Observable contract:

- The waveform CSV must expose these exact signal names: `vin`, `clk`, `rst_n`,
  `vout`, `dout_3`, `dout_2`, `dout_1`, `dout_0`.
- If the implementation uses a bus internally, make the testbench save each bit
  under the scalar names above.

Minimum simulation goal:

- vdd=0.9 V, 1 GHz sampling clock, ramp input from 0 to vdd over 50 ns,
  reset deasserts at ~10 ns, run for 50 ns
- ADC must exercise at least 14 distinct output codes
- `vout` must stay within [0, vdd]
- quantization error (code×vstep − vin at sample instants) must be in (−lstep, 0]

Ports:

ADC module `adc_ideal_4b`:
- `vin`: input electrical
- `clk`: input electrical
- `vdd`: input electrical
- `vss`: input electrical
- `rst_n`: input electrical
- `dout[3:0]`: output electrical bus

DAC module `dac_ideal_4b`:
- `din[3:0]`: input electrical bus
- `vdd`: input electrical
- `vss`: input electrical
- `rst_n`: input electrical
- `vout`: output electrical

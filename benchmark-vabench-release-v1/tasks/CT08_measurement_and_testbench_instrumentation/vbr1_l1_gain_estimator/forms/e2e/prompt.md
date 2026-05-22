# Task: vbr1_l1_gain_estimator:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Measurement and Testbench Instrumentation
- Base function: Gain estimator
- Domain: `voltage`
- Target artifact(s): `dither_adder.va`, `gain_amp_fixed.va`, `lfsr.va`, `tb_gain_extraction_ref.scs`, `vin_src.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `dither_adder.va`, `gain_amp_fixed.va`, `lfsr.va`, `tb_gain_extraction_ref.scs`, `vin_src.va`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

Return exactly these source artifacts:

- `dither_adder.va`
- `gain_amp_fixed.va`
- `lfsr.va`
- `tb_gain_extraction_ref.scs`
- `vin_src.va`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a minimal voltage-domain gain extraction smoke system and one EVAS-compatible Spectre testbench.

# Task: gain_extraction_smoke

## Objective

Create a dither-based gain extraction signal path whose output differential swing is measurably
larger than the input differential swing. The checker measures waveform statistics, not an internal
estimator code.

## Required Verilog-A Modules

Return these Verilog-A modules:

1. `vin_src`
   - Ports: `clk`, `rst_n`, `vinp`, `vinn`
   - Generates a small differential voltage stimulus after reset.
2. `lfsr`
   - Ports: `dpn`, `vdd`, `vss`, `clk`, `en`, `rst_n`
   - Produces a 1-bit pseudo-random dither sign signal on `dpn`.
3. `dither_adder`
   - Ports: `vinp`, `vinn`, `dpn`, `vdin_p`, `vdin_n`
   - Adds `+/-DITHER_AMP` to the differential input according to `dpn`.
4. `gain_amp_fixed`
   - Ports: `vdin_p`, `vdin_n`, `vamp_p`, `vamp_n`
   - Applies a configurable differential gain.

Do not create a `gain_estimator` module for this task; the EVAS checker estimates gain from saved
waveforms.

## Behavioral Contract

- Use pure voltage-domain Verilog-A only.
- Use `@(cross(...))` for clocked state updates.
- Use `transition(...)` for digital-like outputs.
- `gain_amp_fixed` should support parameter `ACTUAL_GAIN`.
- `dither_adder` should support parameter `DITHER_AMP`.
- `vin_src` should support enough parameterization to generate a small clocked differential input stimulus.
- The saved waveforms must satisfy:
  - `std(vamp_p - vamp_n) / std(vinp - vinn) > 4.0`
  - `std(vamp_p - vamp_n) > std(vinp - vinn)`

## Testbench Contract

- Use a 0.9 V supply and 0 V reference.
- Drive a 50 MHz-class clock, active-low reset, and enable signal.
- Instantiate `vin_src`, `lfsr`, `dither_adder`, and `gain_amp_fixed` as a connected signal path.
- Use `ACTUAL_GAIN=8.64` and `DITHER_AMP=0.014063` or equivalent parameters that produce clear gain separation.
- Save these exact scalar names: `vinp`, `vinn`, `vamp_p`, `vamp_n`.

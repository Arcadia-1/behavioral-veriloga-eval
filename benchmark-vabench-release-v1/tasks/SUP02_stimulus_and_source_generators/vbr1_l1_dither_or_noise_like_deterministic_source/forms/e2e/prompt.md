# Task: vbr1_l1_dither_or_noise_like_deterministic_source:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Stimulus and Source Generators
- Base function: Dither or noise-like deterministic source
- Domain: `voltage`
- Target artifact(s): `noise_gen.va`, `noise_gen_ref.va`, `tb_noise_gen_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `noise_gen.va`, `noise_gen_ref.va`, `tb_noise_gen_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `noise_gen.va` declares module `noise_gen` with positional ports: `vin_i`, `vout_o`.
- `noise_gen_ref.va` declares module `noise_gen` with positional ports: `vin_i`, `vout_o`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=500n maxstep=1n
```

The release harness expects these exact public scalar observables:

- `vin_i`
- `vout_o`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vin_i`

## Public Behavior Checks

- `noise_is_nontrivial`
- `noise_std_in_range`

## Output Contract

Return exactly these source artifacts:

- `noise_gen.va`
- `noise_gen_ref.va`
- `tb_noise_gen_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `noise_gen`.

Create a voltage-domain Gaussian noise generator in Verilog-A,
then produce a minimal EVAS-compatible Spectre testbench and run a smoke simulation.

Behavioral intent:

- one analog input `vin_i` and one analog output `vout_o`
- parameter `sigma` (real, in Volts) controls the noise standard deviation
- output = input + zero-mean Gaussian noise: `vout_o = vin_i + sigma * $rdist_normal(...)`
- the noise is independent and added on every time step
- use `transition(...)` to drive `vout_o`

Implementation constraints:

- pure voltage-domain Verilog-A only
- EVAS-compatible syntax
- `$rdist_normal` is the correct EVAS-compatible call for Gaussian samples
- `vin_i` and `vout_o` must appear in the waveform CSV

Minimum simulation goal:

- DC input at 1.0 V, sigma=0.1 V, run for 500 ns with maxstep=0.5 ns
- `vout_o` mean must be within ±0.5 V of `vin_i` (zero-mean noise)
- noise standard deviation (std of `vout_o - vin_i`) must be between 0.01 V and 0.5 V
- `vout_o` must not be identical to `vin_i` (noise must be non-trivial)

Ports:
- `vin_i`: input electrical
- `vout_o`: output electrical

# Task: vbr1_l1_thermometer_code_decoder:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Data Converter Models
- Base function: Thermometer-code decoder
- Domain: `voltage`
- Target artifact(s): `tb_thermometer_decoder_guarded_ref.scs`
- Supplied/reference support artifact(s): `thermometer_decoder_guarded.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `thermometer_decoder_guarded.va` declares module `thermometer_decoder_guarded` with positional ports: `b0`, `b1`, `en`, `th0`, `th1`, `th2`, `th3`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=120n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `b0`
- `b1`
- `en`
- `th0`
- `th1`
- `th2`
- `th3`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `en`
- `b0`
- `b1`

## Public Behavior Checks

- `enable_low_forces_all_low`
- `cumulative_sequence_for_codes_1_2_3`
- `guarded_th3_remains_low`

## Output Contract

Return exactly one source artifact named `tb_thermometer_decoder_guarded_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_thermometer_decoder_guarded_tb

Write a Spectre testbench for a guarded thermometer decoder DUT.

The DUT module is `thermometer_decoder_guarded` with ports `b0, b1, en, th0, th1, th2, th3`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `thermometer_decoder_guarded.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Decode a 2-bit binary input into cumulative thermometer outputs while `en` is high.
- With `en` low, force all thermometer outputs low.
- For codes 1, 2, and 3, assert `th0`, then `th0:th1`, then `th0:th2`; `th3` remains guarded low for this 2-bit input space.

Stimulus and observability requirements:
- Exercise enable-low, code 1, code 2, and code 3 windows.
- Save inputs and all thermometer outputs.

Return exactly one Spectre testbench file named `tb_thermometer_decoder_guarded_ref.scs`.

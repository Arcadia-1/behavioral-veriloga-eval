# Task: vbr1_l1_thermometer_code_decoder:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Data Converter Models
- Base function: Thermometer-code decoder
- Domain: `voltage`
- Target artifact(s): `tb_thermometer_decoder_guarded_ref.scs`, `thermometer_decoder_guarded.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `tb_thermometer_decoder_guarded_ref.scs`, `thermometer_decoder_guarded.va`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

Return exactly these source artifacts:

- `tb_thermometer_decoder_guarded_ref.scs`
- `thermometer_decoder_guarded.va`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_thermometer_decoder_guarded_e2e

Write both the Verilog-A DUT and Spectre testbench for a guarded thermometer decoder.

The DUT module is `thermometer_decoder_guarded` with ports `b0, b1, en, th0, th1, th2, th3`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Decode a 2-bit binary input into cumulative thermometer outputs while `en` is high.
- With `en` low, force all thermometer outputs low.
- For codes 1, 2, and 3, assert `th0`, then `th0:th1`, then `th0:th2`; `th3` remains guarded low for this 2-bit input space.

Required testbench behavior:
- Exercise enable-low, code 1, code 2, and code 3 windows.
- Save inputs and all thermometer outputs.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `thermometer_decoder_guarded.va` and `tb_thermometer_decoder_guarded_ref.scs`.

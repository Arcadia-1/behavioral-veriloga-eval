# Thermometer Code Decoder

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converter Models
- Base function: Thermometer-code decoder
- Domain: `voltage`
- Target artifact(s): `thermometer_decoder_guarded.va`
- Supplied/reference support artifact(s): `tb_thermometer_decoder_guarded_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Output boundary: implement only the requested DUT artifact; validation harnesses and simulator-private hooks are external to the requested output.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `thermometer_decoder_guarded.va` declares module `thermometer_decoder_guarded` with positional ports: `b0`, `b1`, `en`, `th0`, `th1`, `th2`, `th3`.

## Public Testbench And Observable Contract

Public transient context:

```spectre
tran tran stop=120n maxstep=500p
```

The public scalar observables are:

- `b0`
- `b1`
- `en`
- `th0`
- `th1`
- `th2`
- `th3`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `enable_low_forces_all_low`
- `cumulative_sequence_for_codes_1_2_3`
- `guarded_th3_remains_low`

## Output Contract

Return exactly one source artifact named `thermometer_decoder_guarded.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

## Additional Task Details

Write a pure voltage-domain Verilog-A module for a guarded thermometer decoder.

The DUT module is `thermometer_decoder_guarded` with ports `b0, b1, en, th0, th1, th2, th3`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Decode a 2-bit binary input into cumulative thermometer outputs while `en` is high.
- With `en` low, force all thermometer outputs low.
- For codes 1, 2, and 3, assert `th0`, then `th0:th1`, then `th0:th2`; `th3` remains guarded low for this 2-bit input space.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `thermometer_decoder_guarded.va`.

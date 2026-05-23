# Task: vbr1_l1_serializer_frame_aligner:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converters
- Base function: ADC/readout serializer frame aligner
- Domain: `voltage`
- Target artifact(s): `serializer_frame_alignment_ref.va`
- Supplied/reference support artifact(s): `tb_serializer_frame_alignment_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `serializer_frame_alignment_ref.va` declares module `serializer_frame_alignment_ref` with positional ports: `vdd`, `vss`, `clk`, `load`, `din7`, `din6`, `din5`, `din4`, `din3`, `din2`, `din1`, `din0`, `sout`, `frame`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=130n maxstep=0.1n
```

The release harness expects these exact public scalar observables:

- `clk`
- `load`
- `frame`
- `sout`
- `din7`
- `din6`
- `din5`
- `din4`
- `din3`
- `din2`
- `din1`
- `din0`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `frame_pulse_present_for_each_loaded_word`
- `serialized_bits_match_word0xA5_then_0x3C`
- `frame_pulse_width_is_single_bit_window`

## Output Contract

Return exactly one source artifact named `serializer_frame_alignment_ref.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# ADC/readout serializer frame aligner DUT

Write the Verilog-A DUT artifact(s) for `ADC/readout serializer frame aligner`.

This is a function-checked DUT task for serializing a voltage-coded conversion
result, not a generic companion wrapper. The public contract below defines the
exact module interface, voltage-domain behavior, and waveform observables used
by the release checker.

Domain: pure voltage-domain behavioral Verilog-A.

## Module Contract

- Declaration: `serializer_frame_alignment_ref(vdd, vss, clk, load, din7, din6, din5, din4, din3, din2, din1, din0, sout, frame)`

Ports:

- `vdd`, `vss`: electrical supply rails
- `clk`: input electrical shift clock
- `load`: input electrical conversion-result word-load control
- `din7..din0`: input electrical parallel conversion-result data word
- `sout`: output electrical serial data
- `frame`: output electrical first-bit frame marker

## Behavioral Contract

- latch the 8-bit input word when `load` is high on a clock edge
- shift data MSB-first on subsequent clock edges
- assert `frame` for the first serialized bit of each loaded word only

## Public Evaluation Observables

The companion validation testbench saves these waveform columns:

- `clk`
- `frame`
- `sout`

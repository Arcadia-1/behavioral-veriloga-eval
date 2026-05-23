# Task: vbr1_l2_serializer_frame_alignment_flow:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Data Converters
- Base function: Readout frame-monitor flow
- Domain: `voltage`
- Target artifact(s): `serializer_frame_monitor_flow.va`, `tb_serializer_frame_monitor_flow.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `serializer_frame_monitor_flow.va`, `tb_serializer_frame_monitor_flow.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `serializer_frame_monitor_flow.va` declares module `serializer_frame_monitor_flow` with positional ports: `vdd`, `vss`, `clk`, `load`, `din7`, `din6`, `din5`, `din4`, `din3`, `din2`, `din1`, `din0`, `sout`, `frame`, `word_ok`, `frame_error`, `word_mon`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=140n maxstep=0.1n
```

The release harness expects these exact public scalar observables:

- `clk`
- `load`
- `frame`
- `sout`
- `word_ok`
- `frame_error`
- `word_mon`
- `din7`
- `din6`
- `din5`
- `din4`
- `din3`
- `din2`
- `din1`
- `din0`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clk`
- `load`
- `din7`
- `din6`
- `din5`
- `din4`
- `din3`
- `din2`
- `din1`
- `din0`

## Public Behavior Checks

- `frame_pulse_present_for_each_loaded_word`
- `serialized_bits_and_word_monitor_match_expected_words`
- `word_ok_pulses_and_frame_error_stays_low`

## Output Contract

Return exactly these source artifacts:

- `serializer_frame_monitor_flow.va`
- `tb_serializer_frame_monitor_flow.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a pure voltage-domain Verilog-A readout flow named
`serializer_frame_monitor_flow` and a Spectre transient testbench.

The flow composes an ADC/readout serializer with a simple frame monitor:

1. On a rising clock edge with `load` high, latch the 8-bit voltage-coded
   conversion-result word from `din7..din0`.
2. On following clock edges, serialize the latched word MSB-first on `sout`.
3. Assert `frame` only during the first serialized bit of each loaded word.
4. Reconstruct the emitted word internally from the serialized stream.
5. Assert `word_ok` after each complete word when the reconstructed word matches
   the loaded word, keep `frame_error` low for aligned frames, and drive
   `word_mon` to a voltage proportional to the reconstructed byte value.

The public testbench must load two words, `0xA5` followed by `0x3C`, and save
all public observables listed above. Use portable Verilog-A `cross()` event
detection and `transition()` output smoothing. Keep the implementation in the
pure electrical voltage domain; do not use current contributions,
transistor-level devices, AC/noise analysis, `ddt()`, or `idt()`.

Ports:
- `vdd`: inout electrical power rail
- `vss`: inout electrical reference rail
- `clk`: input electrical shift clock
- `load`: input electrical conversion-result word-load control
- `din7..din0`: input electrical parallel conversion-result word
- `sout`: output electrical serial data
- `frame`: output electrical first-bit frame marker
- `word_ok`: output electrical reconstructed-word valid pulse
- `frame_error`: output electrical frame or word mismatch flag
- `word_mon`: output electrical reconstructed-word monitor

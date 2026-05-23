# Task: vbr1_l2_serializer_frame_alignment_flow:tb

## Release Task Contract

- Form: `tb`
- Level: `L2`
- Category: Data Converters
- Base function: Readout frame-monitor flow
- Domain: `voltage`
- Target artifact(s): `tb_serializer_frame_monitor_flow.scs`
- Supplied/reference support artifact(s): `serializer_frame_monitor_flow.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

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

Return exactly one source artifact named `tb_serializer_frame_monitor_flow.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Readout Frame-Monitor Flow Testbench Companion

Write a Spectre transient testbench for the `serializer_frame_monitor_flow`
behavioral Verilog-A release task.

The testbench must instantiate the supplied readout flow, drive `vdd=0.9 V`,
`vss=0 V`, provide a shift clock, and load two voltage-coded conversion-result
words: `0xA5` followed by `0x3C`. Save `clk`, `load`, `frame`, `sout`,
`word_ok`, `frame_error`, `word_mon`, and all `din7..din0` bit inputs using
plain scalar save names. Use one transient analysis matching the public
transient contract. Avoid transistor-level devices, AC/noise analysis, and
current-domain solver assumptions.

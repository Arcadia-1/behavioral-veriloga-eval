# Task: vbr1_l1_serializer_frame_aligner:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Data Converters
- Base function: ADC/readout serializer frame aligner
- Domain: `voltage`
- Target artifact(s): `serializer_frame_alignment_ref.va`, `tb_serializer_frame_alignment_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `serializer_frame_alignment_ref.va`, `tb_serializer_frame_alignment_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

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
- `serialized_bits_match_word0xA5_then_0x3C`
- `frame_pulse_width_is_single_bit_window`

## Output Contract

Return exactly these source artifacts:

- `serializer_frame_alignment_ref.va`
- `tb_serializer_frame_alignment_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a pure voltage-domain ADC/readout ADC/readout parallel-to-serial block with explicit frame alignment signaling.

Module name: `serializer_frame_alignment_ref`.

Requirements:

1. Ports: `vdd`, `vss`, `clk`, `load`, `din[7:0]`, `sout`, `frame`
2. Latch the parallel conversion-result word when `load` is high at a clock edge
3. Shift data out MSB-first on following clock edges
4. Assert `frame` for the first serialized bit of each loaded word
5. Use portable Verilog-A `cross()` event detection and `transition()` output smoothing
6. Keep implementation in pure electrical voltage domain

Ports:
- `vdd`: electrical
- `vss`: electrical
- `clk`: electrical
- `load`: electrical
- `din7`: electrical
- `din6`: electrical
- `din5`: electrical
- `din4`: electrical
- `din3`: electrical
- `din2`: electrical
- `din1`: electrical
- `din0`: electrical
- `sout`: electrical
- `frame`: output electrical first-bit frame marker
- `vss`: inout electrical (power rail)
- `clk`: input electrical
- `load`: input electrical conversion-result word-load control
- `din7`: input electrical conversion-result bit
- `din6`: input electrical
- `din5`: input electrical
- `din4`: input electrical
- `din3`: input electrical
- `din2`: input electrical
- `din1`: input electrical
- `din0`: input electrical
- `sout`: output electrical
- `frame`: output electrical

## Output Contract (MANDATORY)

- Return exactly two fenced code blocks:
  - first block: Verilog-A DUT (` ```verilog-a ... ``` `)
  - second block: Spectre testbench (` ```spectre ... ``` `)
- The Spectre testbench must include the DUT with `ahdl_include "<module>.va"`.
- Use a single `tran` analysis and include the required `save` signals for checker evaluation.

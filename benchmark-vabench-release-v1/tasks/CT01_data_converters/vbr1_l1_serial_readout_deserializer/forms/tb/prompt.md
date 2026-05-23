# Task: vbr1_l1_serial_readout_deserializer:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Data Converters
- Base function: Serial readout deserializer
- Domain: `voltage`
- Target artifact(s): `tb_serial_readout_deserializer.scs`
- Supplied/reference support artifact(s): `serial_readout_deserializer.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public Verilog-A Interface

- `serial_readout_deserializer.va` declares module `serial_readout_deserializer` with positional ports: `vdd`, `vss`, `clk`, `frame`, `serial_in`, `bit3`, `bit2`, `bit1`, `bit0`, `word_valid`, `word_mon`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=120n maxstep=0.2n errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `clk`
- `frame`
- `serial_in`
- `bit3`
- `bit2`
- `bit1`
- `bit0`
- `word_valid`
- `word_mon`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clk`
- `frame`
- `serial_in`

## Public Behavior Checks

- `frame_starts_msb_first_word_capture`
- `word_valid_after_four_serial_bits`
- `word_monitor_matches_reconstructed_words`

## Output Contract

Return exactly one source artifact named `tb_serial_readout_deserializer.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

The public testbench must drive two framed MSB-first serial words, 0x9 followed by 0x6, and save all public observables listed above. The candidate DUT file will be available as `serial_readout_deserializer.va`; include it with `ahdl_include`.

Keep the implementation in the pure electrical voltage domain; do not use current-domain branch contributions, transistor-level devices, AC/noise analysis, `ddt()`, or `idt()`.

# Task: vbr1_l1_serial_readout_deserializer:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Data Converters
- Base function: Serial readout deserializer
- Domain: `voltage`
- Target artifact(s): `serial_readout_deserializer.va`
- Supplied/reference support artifact(s): `tb_serial_readout_deserializer.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

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

Return exactly one source artifact named `serial_readout_deserializer.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a pure voltage-domain Verilog-A module named `serial_readout_deserializer` for a framed ADC/readout serial stream.

On each rising `clk`, `frame` high marks the first MSB of a new 4-bit word on `serial_in`. The next three clocked serial bits complete the word. After the fourth bit, assert `word_valid`, drive `bit3..bit0` with the reconstructed word, and drive `word_mon` proportional to the 4-bit code. A new `frame` starts a new capture and clears the previous valid pulse. Use voltage-domain contributions and smoothed transitions only.

Keep the implementation in the pure electrical voltage domain; do not use current-domain branch contributions, transistor-level devices, AC/noise analysis, `ddt()`, or `idt()`.

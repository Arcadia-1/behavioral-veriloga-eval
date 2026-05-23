# Task: vbr1_l1_adc_code_capture_register:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Data Converters
- Base function: ADC code capture register
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Fix only the supplied buggy Verilog-A DUT; do not generate a testbench or checker.
- Preserve the public module name, port order, parameters, and observable names.

## Public Verilog-A Interface

- `adc_code_capture_register.va` declares module `adc_code_capture_register` with positional ports: `vdd`, `vss`, `clk`, `load`, `over_lo`, `over_hi`, `din3`, `din2`, `din1`, `din0`, `bit3`, `bit2`, `bit1`, `bit0`, `valid`, `overrange`, `code_mon`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=130n maxstep=0.2n errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `clk`
- `load`
- `over_lo`
- `over_hi`
- `din3`
- `din2`
- `din1`
- `din0`
- `bit3`
- `bit2`
- `bit1`
- `bit0`
- `valid`
- `overrange`
- `code_mon`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clk`
- `load`
- `over_lo`
- `over_hi`
- `din3`
- `din2`
- `din1`
- `din0`

## Public Behavior Checks

- `load_captures_parallel_conversion_code`
- `held_code_remains_stable_between_loads`
- `overrange_flag_tracks_clip_inputs`

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a pure voltage-domain Verilog-A module named `adc_code_capture_register` for an ADC/readout boundary.

The module latches a 4-bit voltage-coded conversion result only on rising `clk` edges where `load` is high. It drives latched bit outputs `bit3..bit0`, asserts `valid` after a capture, drives `code_mon` proportional to the captured code, and asserts `overrange` when either `over_lo` or `over_hi` is high at the capture edge. Between load events, the captured code and flags must hold their previous values. Use voltage-domain contributions and smoothed transitions only.

Fault behavior: the buggy implementation updates the captured code on every clock edge even when `load` is low, so the held readout word can drift between conversions.

Keep the implementation in the pure electrical voltage domain; do not use current-domain branch contributions, transistor-level devices, AC/noise analysis, `ddt()`, or `idt()`.

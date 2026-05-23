# Task: vbr1_l1_adc_code_capture_register:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Data Converters
- Base function: ADC code capture register
- Domain: `voltage`
- Target artifact(s): `tb_adc_code_capture_register.scs`
- Supplied/reference support artifact(s): `adc_code_capture_register.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

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

Return exactly one source artifact named `tb_adc_code_capture_register.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

The public testbench must drive at least three capture events: code 0x3, code 0xC to prove hold behavior between loads, and code 0xF with overrange asserted. Save all public observables listed above. The candidate DUT file will be available as `adc_code_capture_register.va`; include it with `ahdl_include`.

Keep the implementation in the pure electrical voltage domain; do not use current-domain branch contributions, transistor-level devices, AC/noise analysis, `ddt()`, or `idt()`.

# Task: vbr1_l1_voltage_clamp_or_limiter:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Voltage clamp or limiter
- Domain: `voltage`
- Target artifact(s): `dut.va`
- Supplied/reference support artifact(s): `tb_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `dut.va` declares module `voltage_clamp` with positional ports: `raw_level`, `vdd`, `vss`, `clamped_level`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=120n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `raw_level`
- `clamped_level`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `below_range_clamps_to_0p18`
- `inside_range_follows_raw_level`
- `above_range_clamps_to_0p72`

## Output Contract

Return exactly one source artifact named `dut.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_voltage_clamp_dut

Write a pure voltage-domain Verilog-A module for a voltage clamp.

The DUT module is `voltage_clamp` with ports `raw_level, vdd, vss, clamped_level`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Clamp `raw_level` to the public range 0.18 V to 0.72 V.
- Drive `clamped_level` through `transition()` using voltage-domain contributions only.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut.va`.

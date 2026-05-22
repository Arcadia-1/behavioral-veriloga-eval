# Task: vbr1_l1_rotating_dem_selector:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Rotating DEM selector
- Domain: `voltage`
- Target artifact(s): `rotating_element_selector.va`
- Supplied/reference support artifact(s): `tb_rotating_element_selector_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `rotating_element_selector.va` declares module `rotating_element_selector` with positional ports: `clk`, `rst_n`, `sel0`, `sel1`, `sel2`, `sel3`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=130n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `clk`
- `rst_n`
- `sel0`
- `sel1`
- `sel2`
- `sel3`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `fixed_time_active_selector_sequence_at_20_40_60_80_100_120ns`
- `expected_sequence_1_2_3_0_1_2`

## Output Contract

Return exactly one source artifact named `rotating_element_selector.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_rotating_element_selector_dut

Write a pure voltage-domain Verilog-A module named `rotating_element_selector`.

The module has electrical ports `clk`, `rst_n`, `sel0`, `sel1`, `sel2`, and
`sel3`. `rst_n` is active low. On reset, return to selector state 0. On each
rising edge of `clk` while reset is released, advance the selector modulo 4.
Exactly one selector output should be high at a time, driven as a 0/0.9 V logic
level with smoothed transitions.

The public observable sequence after reset is released is `sel1`, `sel2`,
`sel3`, `sel0`, then repeat.

Use voltage contributions only. Do not use current contributions, `ddt()`, or
`idt()`.

Return exactly one complete Verilog-A file named `rotating_element_selector.va`.

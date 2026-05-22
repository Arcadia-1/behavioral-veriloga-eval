# Task: vbr1_l1_windowed_dem_pointer:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Windowed DEM pointer
- Domain: `voltage`
- Target artifact(s): `barrel_pointer_window.va`
- Supplied/reference support artifact(s): `tb_barrel_pointer_window_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `barrel_pointer_window.va` declares module `barrel_pointer_window` with positional ports: `clk`, `rst_n`, `win0`, `win1`, `win2`, `win3`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=130n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `clk`
- `rst_n`
- `win0`
- `win1`
- `win2`
- `win3`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `fixed_time_window_sequence_at_20_40_60_80_100_120ns`
- `expected_sequence_12_23_03_01_12_23`

## Output Contract

Return exactly one source artifact named `barrel_pointer_window.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_barrel_pointer_window_dut

Write a pure voltage-domain Verilog-A module named `barrel_pointer_window`.

The module implements a clocked 4-state barrel pointer with two adjacent active
window outputs. Ports are `clk`, `rst_n`, `win0`, `win1`, `win2`, and `win3`.
All ports are electrical. `rst_n` is active low. On reset, return the pointer to
state 0. On each rising edge of `clk` while reset is released, advance the state
modulo 4.

Drive the window outputs as 0/0.9 V logic levels with smoothed voltage
transitions:

- state 0: `win0` and `win1` high
- state 1: `win1` and `win2` high
- state 2: `win2` and `win3` high
- state 3: `win3` and `win0` high

Use voltage contributions only. Do not use current contributions, `ddt()`, or
`idt()`.

Return exactly one complete Verilog-A file named `barrel_pointer_window.va`.

# Task: vbr1_l1_windowed_dem_pointer:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Windowed DEM pointer
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`, `tb_barrel_pointer_window_buggy.scs`, `tb_barrel_pointer_window_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `barrel_pointer_window` with positional ports: `clk`, `rst_n`, `win0`, `win1`, `win2`, `win3`.
- `dut_fixed.va` declares module `barrel_pointer_window` with positional ports: `clk`, `rst_n`, `win0`, `win1`, `win2`, `win3`.

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

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_barrel_pointer_window_bugfix

The provided voltage-domain rotating barrel-pointer window generator has a
window mapping bug: one output duplicates another adjacent window and loses the
wrap-around pair. Fix the design so exactly two adjacent window outputs are high
for each pointer position, including the wrap-around window.

The fixed module must be named `barrel_pointer_window` and use electrical ports
`clk`, `rst_n`, `win0`, `win1`, `win2`, and `win3`. Reset should return the
pointer to its initial state. While reset is released, rising clock edges should
advance the pointer through the four adjacent two-window states.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.

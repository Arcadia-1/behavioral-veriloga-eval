# Task: vbr1_l1_windowed_dem_pointer:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Windowed DEM pointer
- Domain: `voltage`
- Target artifact(s): `tb_barrel_pointer_window_ref.scs`
- Supplied/reference support artifact(s): `barrel_pointer_window.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

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

Public stimulus/source nodes visible in the reference harness include:

- `clk`
- `rst_n`

## Public Behavior Checks

- `fixed_time_window_sequence_at_20_40_60_80_100_120ns`
- `expected_sequence_12_23_03_01_12_23`

## Output Contract

Return exactly one source artifact named `tb_barrel_pointer_window_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_barrel_pointer_window_tb

Write a Spectre testbench for a Verilog-A module named
`barrel_pointer_window` with ports `clk rst_n win0 win1 win2 win3`.

The testbench should exercise an active-low reset followed by several rising
clock edges so the two-adjacent-window sequence can be observed. Save `clk`,
`rst_n`, and all four `win*` outputs. Use a transient stop time long enough to
observe at least six post-reset window states, with `maxstep` small enough for
stable event checking.

Return exactly one Spectre testbench file named `tb_barrel_pointer_window_ref.scs`.

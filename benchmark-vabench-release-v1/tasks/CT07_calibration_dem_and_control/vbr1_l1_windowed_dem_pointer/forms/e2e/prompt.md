# Task: vbr1_l1_windowed_dem_pointer:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Windowed DEM pointer
- Domain: `voltage`
- Target artifact(s): `barrel_pointer_window.va`, `tb_barrel_pointer_window_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `barrel_pointer_window.va`, `tb_barrel_pointer_window_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

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

Public stimulus/source nodes visible in the reference harness include:

- `clk`
- `rst_n`

## Public Behavior Checks

- `fixed_time_window_sequence_at_20_40_60_80_100_120ns`
- `expected_sequence_12_23_03_01_12_23`

## Output Contract

Return exactly these source artifacts:

- `barrel_pointer_window.va`
- `tb_barrel_pointer_window_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_barrel_pointer_window_e2e

Write both the Verilog-A DUT and Spectre testbench for a 4-state barrel pointer
window generator.

The DUT module must be named `barrel_pointer_window` and use ports `clk`,
`rst_n`, `win0`, `win1`, `win2`, and `win3`. All ports are electrical. `rst_n`
is active low. Reset returns the pointer to state 0. Each rising `clk` edge
while reset is released advances the state modulo 4. Exactly two adjacent
window outputs are high in each state: `win0/win1`, then `win1/win2`, then
`win2/win3`, then `win3/win0`.

The testbench must stimulate reset and at least six post-reset clocked states,
save `clk`, `rst_n`, and all `win*` outputs, and run a transient analysis with
sufficient time resolution for event checking.

Return exactly two files: `barrel_pointer_window.va` and `tb_barrel_pointer_window_ref.scs`.

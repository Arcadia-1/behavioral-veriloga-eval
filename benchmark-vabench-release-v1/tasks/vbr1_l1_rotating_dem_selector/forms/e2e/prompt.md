# Task: vbr1_l1_rotating_dem_selector:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Rotating DEM selector
- Domain: `voltage`
- Target artifact(s): `rotating_element_selector.va`, `tb_rotating_element_selector_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `rotating_element_selector.va`, `tb_rotating_element_selector_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

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

Public stimulus/source nodes visible in the reference harness include:

- `clk`
- `rst_n`

## Public Behavior Checks

- `fixed_time_active_selector_sequence_at_20_40_60_80_100_120ns`
- `expected_sequence_1_2_3_0_1_2`

## Output Contract

Return exactly these source artifacts:

- `rotating_element_selector.va`
- `tb_rotating_element_selector_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_rotating_element_selector_e2e

Write both the Verilog-A DUT and Spectre testbench for a rotating one-hot
element selector.

The DUT module must be named `rotating_element_selector` and use electrical
ports `clk`, `rst_n`, `sel0`, `sel1`, `sel2`, and `sel3`. `rst_n` is active low.
After reset, successive rising clock edges should produce the active selector
sequence `sel1`, `sel2`, `sel3`, `sel0`, then repeat.

The testbench must stimulate reset and enough rising clock edges to observe at
least six post-reset states, save all public observables, and run a transient
analysis suitable for fixed-time sequence checks.

Return exactly two files: `rotating_element_selector.va` and `tb_rotating_element_selector_ref.scs`.

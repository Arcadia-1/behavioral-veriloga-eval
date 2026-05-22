# Task: vbr1_l1_rotating_dem_selector:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Rotating DEM selector
- Domain: `voltage`
- Target artifact(s): `tb_rotating_element_selector_ref.scs`
- Supplied/reference support artifact(s): `rotating_element_selector.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

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

Return exactly one source artifact named `tb_rotating_element_selector_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_rotating_element_selector_tb

Write a Spectre testbench for a Verilog-A module named
`rotating_element_selector` with ports `clk rst_n sel0 sel1 sel2 sel3`.

The testbench should apply an active-low reset and then clock the DUT through at
least six observable post-reset states. Save `clk`, `rst_n`, and all four
selector outputs. Use a transient analysis with enough stop time and maxstep
resolution for fixed-time one-hot sequence checking.

Return exactly one Spectre testbench file named `tb_rotating_element_selector_ref.scs`.

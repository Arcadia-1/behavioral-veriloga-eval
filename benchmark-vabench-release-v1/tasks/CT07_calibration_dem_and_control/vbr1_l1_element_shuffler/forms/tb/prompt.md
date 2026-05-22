# Task: vbr1_l1_element_shuffler:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Element shuffler
- Domain: `voltage`
- Target artifact(s): `tb_element_shuffler_ref.scs`
- Supplied/reference support artifact(s): `element_shuffler.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `element_shuffler.va` declares module `element_shuffler` with positional ports: `clk`, `rst_n`, `out0`, `out1`, `out2`, `out3`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=130n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `clk`
- `rst_n`
- `out0`
- `out1`
- `out2`
- `out3`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `clk`
- `rst_n`

## Public Behavior Checks

- `fixed_time_active_output_sequence_at_20_40_60_80_100_120ns`
- `expected_sequence_1_2_3_0_1_2`

## Output Contract

Return exactly one source artifact named `tb_element_shuffler_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_element_shuffler_tb

Write a Spectre testbench for a Verilog-A module named `element_shuffler` with
ports `clk rst_n out0 out1 out2 out3`.

The testbench should apply an active-low reset and then clock the DUT through at
least six observable post-reset states. Save `clk`, `rst_n`, and all four
outputs. Use a transient analysis with enough stop time and maxstep resolution
for fixed-time one-hot sequence checking.

Return exactly one Spectre testbench file named `tb_element_shuffler_ref.scs`.

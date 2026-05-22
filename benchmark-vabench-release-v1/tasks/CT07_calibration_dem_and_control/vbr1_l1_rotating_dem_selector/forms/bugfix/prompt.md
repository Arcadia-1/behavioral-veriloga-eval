# Task: vbr1_l1_rotating_dem_selector:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Calibration, DEM, and Control
- Base function: Rotating DEM selector
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`, `rotating_element_selector.va`, `tb_rotating_element_selector_buggy.scs`, `tb_rotating_element_selector_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `rotating_element_selector` with positional ports: `clk`, `rst_n`, `sel0`, `sel1`, `sel2`, `sel3`.
- `dut_fixed.va` declares module `rotating_element_selector` with positional ports: `clk`, `rst_n`, `sel0`, `sel1`, `sel2`, `sel3`.
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

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_rotating_element_selector_bugfix

Repair the provided Verilog-A rotating element selector. The DUT has one clock
input `clk`, an active-low reset input `rst_n`, and four voltage-domain one-hot
outputs `sel0`, `sel1`, `sel2`, and `sel3`.

After reset is released, each rising edge of `clk` increments the selector and
wraps after state 3. The public output sequence sampled after the first six
rising edges must be:

`sel1, sel2, sel3, sel0, sel1, sel2`.

Keep outputs voltage-domain only and drive them with `transition`. Do not use
current contributions.

Return exactly one complete Verilog-A file named `dut_fixed.va`.

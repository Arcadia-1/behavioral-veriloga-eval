# Task: vbr1_l1_threshold_comparator:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: Threshold comparator
- Domain: `voltage`
- Target artifact(s): `comparator.va`, `tb_comparator_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `comparator.va`, `tb_comparator_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `comparator.va` declares module `comparator` with positional ports: `VDD`, `VSS`, `VINP`, `VINN`, `OUT_P`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=30n maxstep=0.5n
```

The release harness expects these exact public scalar observables:

- `vinp`
- `vinn`
- `out_p`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `vinp`
- `vinn`

## Public Behavior Checks

- `output_flips_with_input_order`

## Output Contract

Return exactly these source artifacts:

- `comparator.va`
- `tb_comparator_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `comparator`.

Create a voltage-domain comparator in Verilog-A, then produce a minimal EVAS
testbench and run a smoke simulation.

Behavioral intent:

- differential comparison
- output toggles high/low with supply-referenced logic levels
- finite output edge transition
- threshold crossing should be visible in the waveform

Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `VINP`: input electrical
- `VINN`: input electrical
- `OUT_P`: output electrical

# Task: vbr1_l1_strongarm_style_latch_comparator:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: StrongARM-style latch comparator
- Domain: `voltage`
- Target artifact(s): `tb_cmp_strongarm_ref.scs`
- Supplied/reference support artifact(s): `cmp_strongarm.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `cmp_strongarm.va` declares module `cmp_strongarm` with positional ports: `CLK`, `VINN`, `VINP`, `DCMPN`, `DCMPP`, `LP`, `LM`, `VSS`, `VDD`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=4n maxstep=5p
```

The release harness expects these exact public scalar observables:

- `clk`
- `vinp`
- `vinn`
- `out_p`
- `out_n`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `gnd`
- `clk`
- `vinp`
- `vinn`

## Public Behavior Checks

- `outputs_toggle_nontrivially`
- `decision_samples_at_0p75_1p75_2p75_3p75ns_match_PPNN`

## Output Contract

Return exactly one source artifact named `tb_cmp_strongarm_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_strongarm_comparator_behavior_tb

Write a Spectre testbench for a Verilog-A module named `cmp_strongarm` with
ports `CLK VINN VINP DCMPN DCMPP LP LM VSS VDD`.

The testbench should provide 0.9 V supply rails, a 1 GHz clock, and a small
differential input around common-mode 0.45 V. The input polarity should be
positive for the first two clock decisions and negative for the next two. Save
the clock, differential inputs, and comparator outputs using plain signal names.
Use a transient stop time that is not exactly on the final input transition.

Return exactly one Spectre testbench file named `tb_cmp_strongarm_ref.scs`.

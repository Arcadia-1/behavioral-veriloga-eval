# Task: vbr1_l1_strongarm_style_latch_comparator:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: StrongARM-style latch comparator
- Domain: `voltage`
- Target artifact(s): `cmp_strongarm.va`
- Supplied/reference support artifact(s): `tb_cmp_strongarm_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

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

## Public Behavior Checks

- `outputs_toggle_nontrivially`
- `decision_samples_at_0p75_1p75_2p75_3p75ns_match_PPNN`

## Output Contract

Return exactly one source artifact named `cmp_strongarm.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_strongarm_comparator_behavior_dut

Write a pure voltage-domain Verilog-A module named `cmp_strongarm`.

The module is a clocked StrongArm-style comparator with electrical ports
`CLK`, `VINN`, `VINP`, `DCMPN`, `DCMPP`, `LP`, `LM`, `VSS`, and `VDD`. On each
rising edge of `CLK`, compare `VINP - VINN` after applying the optional
`voffset` parameter. Drive `DCMPP` high and `DCMPN` low when the offset-adjusted
differential input is positive; drive `DCMPN` high and `DCMPP` low when it is
negative. On falling clock edges, reset both comparator outputs low.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `cmp_strongarm.va`.

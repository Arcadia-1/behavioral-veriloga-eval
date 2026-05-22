# Task: vbr1_l1_clocked_comparator:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: Clocked comparator
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
tran tran stop=4.25n maxstep=5p
```

The release harness expects these exact public scalar observables:

- `clk`
- `vinp`
- `vinn`
- `out_p`
- `out_n`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `behavioral_module_present`
- `companion_testbench_available`
- `voltage_domain_outputs`

## Output Contract

Return exactly one source artifact named `cmp_strongarm.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Clocked comparator DUT Companion

Write the Verilog-A DUT for this behavioral release task.

This task form is materialized from the already source-controlled `e2e`
release gold for `Clocked comparator`. It exists to make the public
benchmark split complete without inventing a new circuit kernel or a fake
bugfix.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- preserve the public module name and ports used by the companion validation testbench
- implement the pure voltage-domain behavioral function
- drive public outputs with bounded voltage-domain behavior
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

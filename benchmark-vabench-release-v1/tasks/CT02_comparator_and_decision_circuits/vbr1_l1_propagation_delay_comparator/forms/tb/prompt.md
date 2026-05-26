# Task: vbr1_l1_propagation_delay_comparator:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: Comparator and Decision Circuits
- Base function: Propagation-delay comparator
- Domain: `voltage`
- Target artifact(s): `tb_cmp_delay_ref.scs`
- Supplied/reference support artifact(s): `cmp_delay.va`, `edge_interval_timer.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `cmp_delay.va` declares module `cmp_delay` with positional ports: `CLK`, `VINN`, `VINP`, `DCMPN`, `DCMPP`, `LP`, `LM`, `VSS`, `VDD`.
- `edge_interval_timer.va` declares module `edge_interval_timer` with positional ports: `CLK_1`, `CLK_2`, `OUT_PS`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=16n maxstep=10p
```

The release harness expects these exact public scalar observables:

- `clk`
- `vinp`
- `vinn`
- `out_p`
- `out_n`
- `delay_ps`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `gnd`
- `clk`
- `vinp`
- `vinn`

## Public Behavior Checks

- `output_goes_high_in_each_phase`
- `clk_to_output_delay_increases_as_diff_shrinks`

## Output Contract

Return exactly one source artifact named `tb_cmp_delay_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Propagation-delay comparator Testbench Companion

Write a Spectre transient testbench for the supplied `Propagation-delay
comparator` behavioral Verilog-A release task. This is the
testbench-generation companion for an already materialized DUT and timer.

The testbench should instantiate `cmp_delay` and `edge_interval_timer`, drive
the public four-phase differential scenario, save the observable waveform and
metric signals, and preserve the EVAS/Spectre validation contract.

Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include `cmp_delay.va` and `edge_interval_timer.va` via `ahdl_include`
- instantiate `cmp_delay` with scalar nodes `clk`, `vinn`, `vinp`, `out_n`,
  `out_p`, `lp_int`, `lm_int`, `gnd`, and `vdd`
- instantiate `edge_interval_timer` to measure `clk` to `out_p` as `delay_ps`
- provide `vdd=0.9 V`, `gnd=0 V`, and a 1 GHz clock
- apply four positive-polarity phases: `+10 mV`, `+1 mV`, `+0.1 mV`, and
  `+0.01 mV`
- run `tran tran stop=16n maxstep=10p`
- save `clk`, `vinp`, `vinn`, `out_p`, `out_n`, and `delay_ps`
- make the measured clock-to-output delay grow as the differential input
  shrinks across the four phases
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

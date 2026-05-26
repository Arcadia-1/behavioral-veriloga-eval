# Task: vbr1_l1_propagation_delay_comparator:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Comparator and Decision Circuits
- Base function: Propagation-delay comparator
- Domain: `voltage`
- Target artifact(s): `cmp_delay.va`, `edge_interval_timer.va`, `tb_cmp_delay_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `cmp_delay.va`, `edge_interval_timer.va`, `tb_cmp_delay_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

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

Return exactly these source artifacts:

- `cmp_delay.va`
- `edge_interval_timer.va`
- `tb_cmp_delay_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a compact voltage-domain propagation-delay comparator benchmark.

The DUT module `cmp_delay` must use the public uppercase formal ports listed
above. The Spectre testbench should connect those ports positionally to scalar
testbench nodes named `clk`, `vinn`, `vinp`, `out_n`, `out_p`, `lp_int`,
`lm_int`, `gnd`, and `vdd`, then save the public scalar observables.

Behavioral requirements:

- detect each rising edge of `CLK`
- compare `V(VINP) - V(VINN)`
- drive `DCMPP`/`DCMPN` as complementary rail-referenced decisions using
  `transition()`
- reset the public decision outputs low between decisions
- make the positive-output clock-to-output delay grow as
  `abs(V(VINP)-V(VINN))` shrinks across the four public phases
- keep `LP` and `LM` as compatibility monitor ports; the checker observes the
  saved scalar aliases `out_p`, `out_n`, and `delay_ps`

The testbench must:

- include `cmp_delay.va` and `edge_interval_timer.va` via `ahdl_include`
- provide `vdd=0.9 V` and `gnd=0 V`
- generate a 1 GHz clock with a rising edge near 0.1 ns in each 1 ns cycle
- apply four positive-polarity differential phases:
  `+10 mV`, `+1 mV`, `+0.1 mV`, and `+0.01 mV`
- instantiate `edge_interval_timer` to measure `clk` to `out_p` as `delay_ps`
- run `tran tran stop=16n maxstep=10p`
- save exactly the public scalar observables `clk`, `vinp`, `vinn`, `out_p`,
  `out_n`, and `delay_ps`

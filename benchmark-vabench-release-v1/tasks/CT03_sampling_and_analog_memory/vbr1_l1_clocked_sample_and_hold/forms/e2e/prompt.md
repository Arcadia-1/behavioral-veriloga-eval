# Task: vbr1_l1_clocked_sample_and_hold:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Sampling and Analog Memory
- Base function: Clocked sample-and-hold
- Domain: `voltage`
- Target artifact(s): `sample_hold.va`, `tb_sample_hold_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `sample_hold.va`, `tb_sample_hold_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `sample_hold.va` declares module `sample_hold` with positional ports: `VDD`, `VSS`, `IN`, `CLK`, `OUT`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=1u maxstep=2n
```

The release harness expects these exact public scalar observables:

- `in`
- `clk`
- `out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `in`
- `clk`

## Public Behavior Checks

- `sh_output_tracks_input_at_edges`
- `sh_output_held_between_edges`

## Output Contract

Return exactly these source artifacts:

- `sample_hold.va`
- `tb_sample_hold_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a pure voltage-domain Verilog-A clocked sample-and-hold and its Spectre
transient testbench.

The DUT module must be named `sample_hold` and use positional electrical ports
`VDD`, `VSS`, `IN`, `CLK`, and `OUT`. On each rising `CLK` threshold crossing,
the model samples `V(IN)` and holds that value on `OUT` until the next rising
clock edge. The output should be driven with bounded `transition(...)` behavior
and should not continuously track `IN` between sample events.

The testbench must include `sample_hold.va`, provide 0.9 V/0 V supplies, drive a
varying input and repeated clock edges, run transient analysis, and save exactly
`in`, `clk`, and `out`.

Use voltage contributions only. Do not use current contributions, `ddt()`, or
`idt()`.

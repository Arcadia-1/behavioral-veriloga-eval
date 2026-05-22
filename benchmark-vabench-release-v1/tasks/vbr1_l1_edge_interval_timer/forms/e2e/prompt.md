# Task: vbr1_l1_edge_interval_timer:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Measurement and Testbench Instrumentation
- Base function: Edge interval timer
- Domain: `voltage`
- Target artifact(s): `cross_interval_163p333_ref.va`, `tb_cross_interval_163p333_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `cross_interval_163p333_ref.va`, `tb_cross_interval_163p333_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `cross_interval_163p333_ref.va` declares module `cross_interval_163p333_ref` with positional ports: `VDD`, `VSS`, `a`, `b`, `delay_out`, `seen_out`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=12n maxstep=5p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `a`
- `b`
- `delay_out`
- `seen_out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`
- `a`
- `b`

## Public Behavior Checks

- `cross_interval_163p333`

## Output Contract

Return exactly these source artifacts:

- `cross_interval_163p333_ref.va`
- `tb_cross_interval_163p333_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `cross_interval_163p333_ref`.

# Task: cross_interval_163p333_smoke

## Objective

Write a Verilog-A event-time interval probe that records the elapsed time between two rising `cross()` events.

## Specification

- **Module name**: `cross_interval_163p333_ref`
- **Ports**: `VDD`, `VSS`, `a`, `b`, `delay_out`, `seen_out` - all `electrical`
- **Behavior**:
  - Wait for a rising `cross()` on input `a` at threshold `0.45 V`; record `t_a = $abstime`.
  - Wait for a rising `cross()` on input `b` at threshold `0.45 V`; record `t_b = $abstime`.
  - Output the measured interval `(t_b - t_a)` scaled as `delay_out = VDD * delay_ps / 200`, where `delay_ps` is in ps.
  - Drive `seen_out` HIGH after both crossings have been observed.
  - The reference testbench places the two crossing centers `163.333 ps` apart.

## Constraints

- .., +1))` and `$abstime` inside the event bodies.
- ..)` for outputs.
- Pure voltage-domain only.
- No `I() <+`, `ddt()`, `idt()`, or matrix/current-domain constructs.

Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `a`: input electrical
- `b`: input electrical
- `delay_out`: output electrical
- `seen_out`: output electrical

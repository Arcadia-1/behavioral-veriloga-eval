# Task: vbr1_l2_event_controller:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: Digital and Event-Driven Logic
- Base function: Event controller
- Domain: `voltage`
- Target artifact(s): `simultaneous_event_order_ref.va`, `tb_simultaneous_event_order_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `simultaneous_event_order_ref.va`, `tb_simultaneous_event_order_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `simultaneous_event_order_ref.va` declares module `simultaneous_event_order_ref` with positional ports: `VDD`, `VSS`, `ref`, `out`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=80n maxstep=20p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `ref`
- `out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`
- `ref`

## Public Behavior Checks

- `ref_edges_align_with_absolute_timer_grid`
- `plateau_levels_encode_cross_after_timer_order`
- `simultaneous_event_order`

## Output Contract

Return exactly these source artifacts:

- `simultaneous_event_order_ref.va`
- `tb_simultaneous_event_order_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `simultaneous_event_order_ref`.

# Task: simultaneous_event_order_smoke

## Objective

Write a Verilog-A model where an absolute timer event and a `cross()` event happen at the same nominal times, and the final plateau level reveals the execution order.

Public behavior requirements:
- The Spectre testbench should drive `VDD=0.9 V`, `VSS=0 V`, and a `ref` pulse train whose rising edges occur at 10 ns, 30 ns, 50 ns, and 70 ns.
- The DUT should schedule absolute timer events on the same 10 ns + 20 ns grid.
- After each same-time timer/cross event pair, `out` should settle to approximately 20%, 40%, 60%, and 80% of `VDD`, respectively.
- Use voltage-domain contributions and smooth transitions; do not use current-domain branch contributions.

Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `ref`: input electrical
- `out`: output electrical

## Output Contract (MANDATORY)

- Return exactly two fenced code blocks:
  - first block: Verilog-A DUT (` ```verilog-a ... ``` `)
  - second block: Spectre testbench (` ```spectre ... ``` `)
- The Spectre testbench must include the DUT with `ahdl_include "<module>.va"`.
- Use a single `tran` analysis and include the required `save` signals for checker evaluation.

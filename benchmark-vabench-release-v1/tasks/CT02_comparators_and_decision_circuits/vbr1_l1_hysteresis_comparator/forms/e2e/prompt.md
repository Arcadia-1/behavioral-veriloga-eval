# Task: vbr1_l1_hysteresis_comparator:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: Hysteresis comparator
- Domain: `voltage`
- Target artifact(s): `cmp_hysteresis.va`, `tb_cmp_hysteresis_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `cmp_hysteresis.va`, `tb_cmp_hysteresis_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `cmp_hysteresis.va` declares module `cmp_hysteresis` with positional ports: `VINN`, `VINP`, `OUTN`, `OUTP`, `VSS`, `VDD`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=80n maxstep=100p
```

The release harness expects these exact public scalar observables:

- `vinp`
- `vinn`
- `out_p`
- `out_n`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `gnd`
- `vinp`
- `vinn`

## Public Behavior Checks

- `output_shows_hysteresis_window`
- `upward_and_downward_trip_points_are_separated`

## Output Contract

Return exactly these source artifacts:

- `cmp_hysteresis.va`
- `tb_cmp_hysteresis_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `cmp_hysteresis` and one minimal voltage-domain Spectre transient testbench.

# Task: comparator_hysteresis_smoke

## Objective

Create a pure voltage-domain differential comparator with hysteresis. The testbench must drive the
differential input through both hysteresis thresholds so both output states are observable.

## DUT Contract

- Module name: `cmp_hysteresis`
- Ports, all `electrical`, exactly in this order: `vinn`, `vinp`, `out_n`, `out_p`, `vss`, `vdd`
- Parameters:
  - `vhys` real, default `10e-3`
  - `tedge` real, default `50p`
- Behavior:
  - Rising decision threshold: `V(vinp) - V(vinn) > +vhys/2` drives `out_p` HIGH and `out_n` LOW.
  - Falling decision threshold: `V(vinp) - V(vinn) < -vhys/2` drives `out_p` LOW and `out_n` HIGH.
  - Between thresholds, hold the previous decision.
  - Use two separate `@(cross(...))` events for rising and falling thresholds.
  - Output HIGH should track `V(vdd)` and output LOW should track `V(vss)`.
  - Drive outputs with `transition(...)`.

## Testbench Contract

- Use a 0.9 V supply and 0 V reference.
- Drive `vinp` and `vinn` so the differential input crosses both `+vhys/2` and `-vhys/2` within the final validation window.
- Instantiate the DUT by positional ports.
- Save these exact scalar names: `vinp`, `vinn`, `out_p`, `out_n`.
- Include the generated DUT file `cmp_hysteresis.va`.

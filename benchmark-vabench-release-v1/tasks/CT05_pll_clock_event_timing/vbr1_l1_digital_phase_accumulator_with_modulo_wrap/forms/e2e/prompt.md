# Task: vbr1_l1_digital_phase_accumulator_with_modulo_wrap:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: PLL / Clock / Event Timing
- Base function: Digital phase accumulator with modulo wrap
- Domain: `voltage`
- Target artifact(s): `phase_accumulator_timer_wrap_ref.va`, `tb_phase_accumulator_timer_wrap_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `phase_accumulator_timer_wrap_ref.va`, `tb_phase_accumulator_timer_wrap_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `phase_accumulator_timer_wrap_ref.va` declares module `phase_accumulator_timer_wrap_ref` with positional ports: `VDD`, `VSS`, `clk_out`, `phase_out`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=75n maxstep=20p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `clk_out`
- `phase_out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`

## Public Behavior Checks

- `phase_accumulator_timer_wrap`

## Output Contract

Return exactly these source artifacts:

- `phase_accumulator_timer_wrap_ref.va`
- `tb_phase_accumulator_timer_wrap_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write an ADPLL-style wrapped phase accumulator and matching transient testbench.

Module name: `phase_accumulator_timer_wrap_ref`.

Required DUT behavior:

- Ports are exactly `VDD`, `VSS`, `clk_out`, `phase_out`.
- Advance the internal phase state on a periodic `@(timer(...))` schedule.
- Wrap phase manually at 1.0 rather than relying on unsupported analog
  integration.
- Drive `phase_out` as a voltage-domain monitor of the wrapped phase state.
- Derive `clk_out` from the wrapped phase state so clock edges are observable
  across multiple wraps.
- Use voltage contributions and `transition()` only.

Required testbench behavior:

- Provide supply rails and save plain scalar observables `clk_out` and
  `phase_out`.
- Run long enough to show at least three phase wraps and corresponding clock
  transitions.

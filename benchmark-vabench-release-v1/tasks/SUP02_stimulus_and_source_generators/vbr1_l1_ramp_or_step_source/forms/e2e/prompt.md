# Task: vbr1_l1_ramp_or_step_source:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Stimulus and Source Generators
- Base function: Periodic phase-ramp guard source
- Domain: `voltage`
- Target artifact(s): `bound_step_period_guard_ref.va`, `tb_bound_step_period_guard_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `bound_step_period_guard_ref.va`, `tb_bound_step_period_guard_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `bound_step_period_guard_ref.va` declares module `bound_step_period_guard_ref` with positional ports: `VDD`, `VSS`, `guard_out`, `phase_out`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=34n maxstep=20n errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `guard_out`
- `phase_out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`

## Public Behavior Checks

- `periodic_phase_ramp_guard_pulse`

## Output Contract

Return exactly these source artifacts:

- `bound_step_period_guard_ref.va`
- `tb_bound_step_period_guard_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `bound_step_period_guard_ref`.

# Task: bound_step_period_guard_smoke

## Objective

Write a Verilog-A periodic phase-ramp source with a guard pulse at the start of each cycle. This is a source/timing primitive benchmark: the public behavior is the phase ramp, period wrap, and guard-pulse timing, not the `$bound_step()` implementation detail alone.

## Specification

- **Module name**: `bound_step_period_guard_ref`
- **Ports**: `VDD`, `VSS`, `guard_out`, `phase_out` - all `electrical`
- **Behavior**:
  - Track an internal cycle boundary every `8 ns` using `@(timer(next_cycle))`.
  - Request `$bound_step(period / 16)` continuously so the waveform remains observable with coarse outer transient settings.
  - Drive `guard_out` HIGH only during the first `1.5 ns` of each cycle, then LOW for the rest of the period.
  - Drive `phase_out` as a normalized `0..VDD` ramp within each cycle so resets are externally visible.
- **Testbench intent**:
  - The supplied testbench uses a coarse `tran maxstep=20n`.
  - The checker validates the source behavior: repeated wraps, guard pulses, and a visible ramp.

## Constraints

- Use `@(initial_step)`, `@(timer(...))`, `$bound_step(...)`, and `transition(...)`.
- Pure voltage-domain only.
- No `I() <+`, `ddt()`, or `idt()`.
- Do not claim solver-level equivalence beyond bounded-step event consistency.

Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `guard_out`: output electrical
- `phase_out`: output electrical

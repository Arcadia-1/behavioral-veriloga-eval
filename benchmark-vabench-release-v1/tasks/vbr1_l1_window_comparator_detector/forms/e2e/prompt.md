# Task: vbr1_l1_window_comparator_detector:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: Window comparator/detector
- Domain: `voltage`
- Target artifact(s): `cross_hysteresis_window_ref.va`, `tb_cross_hysteresis_window_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `cross_hysteresis_window_ref.va`, `tb_cross_hysteresis_window_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `cross_hysteresis_window_ref.va` declares module `cross_hysteresis_window_ref` with positional ports: `VDD`, `VSS`, `vin`, `out`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=90n maxstep=20p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `vin`
- `out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`
- `vin`

## Public Behavior Checks

- `cross_hysteresis_window`

## Output Contract

Return exactly these source artifacts:

- `cross_hysteresis_window_ref.va`
- `tb_cross_hysteresis_window_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `cross_hysteresis_window_ref`.

# Task: cross_hysteresis_window_smoke

## Objective

Write a Verilog-A hysteresis element that uses directional `cross()` events to switch HIGH and LOW at different thresholds.

## Specification

- **Module name**: `cross_hysteresis_window_ref`
- **Ports**: `vin`, `out`, `VDD`, `VSS` - all `electrical`
- **Behavior**:
  - Output starts LOW.
  - When `vin` rises above `0.6 V`, output becomes HIGH.
  - When `vin` falls below `0.3 V`, output becomes LOW.
  - Between thresholds, hold the previous state.
  - Drive output with `transition(...)`.

## Constraints

- .., +1))`, `@(cross(..., -1))`, and `@(initial_step)`.
- Pure voltage-domain only.
- No `I() <+`, `ddt()`, or `idt()`.

Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `vin`: input electrical
- `out`: output electrical

## Output Contract (MANDATORY)

- Return exactly two fenced code blocks:
  - first block: Verilog-A DUT (` ```verilog-a ... ``` `)
  - second block: Spectre testbench (` ```spectre ... ``` `)
- The Spectre testbench must include the DUT with `ahdl_include "<module>.va"`.
- Use a single `tran` analysis and include the required `save` signals for checker evaluation.

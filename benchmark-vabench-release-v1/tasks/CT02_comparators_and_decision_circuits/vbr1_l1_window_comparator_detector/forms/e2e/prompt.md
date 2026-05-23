# Task: vbr1_l1_window_comparator_detector:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: Window comparator/detector
- Domain: `voltage`
- Target artifact(s): `window_comparator_ref.va`, `tb_window_comparator_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `window_comparator_ref.va`, `tb_window_comparator_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `window_comparator_ref.va` declares module `window_comparator_ref` with positional ports: `VDD`, `VSS`, `vin`, `out`.

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

- `true_window_comparator`

## Output Contract

Return exactly these source artifacts:

- `window_comparator_ref.va`
- `tb_window_comparator_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `window_comparator_ref` and a Spectre testbench named `tb_window_comparator_ref.scs`.

# Task: window_comparator_smoke

## Objective

Implement a true window comparator: the output is HIGH only while the input voltage lies between a lower and an upper threshold, and LOW outside that range.

## Specification

- **Module name**: `window_comparator_ref`
- **Ports**: `vin`, `out`, `VDD`, `VSS` - all `electrical`
- **Thresholds**: `vlow = 0.3 V`, `vhigh = 0.6 V`
- **Behavior**:
  - Initialize the decision from the initial value of `V(vin,VSS)`.
  - Drive `out` HIGH only when `vlow < V(vin,VSS) < vhigh`.
  - Drive `out` LOW when `V(vin,VSS) <= vlow` or `V(vin,VSS) >= vhigh`.
  - Use directional `@(cross(...))` events for both thresholds and both ramp directions.
  - Drive the output decision with `transition(...)`, multiplying by the rail voltage outside the `transition(...)` call.

## Testbench Requirements

- Use a single triangular PWL stimulus on `vin` that sweeps below the lower threshold, through the window, above the upper threshold, and back down through the window.
- Use `VDD = 0.9 V`, `VSS = 0 V`.
- Include the DUT with `ahdl_include "./window_comparator_ref.va"`.
- Run `tran tran stop=90n maxstep=20p errpreset=conservative`.
- Save plain scalar observables `vin` and `out`.

## Constraints

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

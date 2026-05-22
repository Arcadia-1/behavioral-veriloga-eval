# Task: vbr1_l1_clocked_sample_and_hold:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Sample, Hold, and Analog Memory
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

Write a Verilog-A module named `sample_hold`.

# Task: sample_hold_smoke

## Objective

Create a clocked sample-and-hold (S&H) circuit behavioral model in Verilog-A
and a minimal EVAS-compatible Spectre testbench.

## Specification

- **Module name**: `sample_hold`
- **Ports** (all `electrical`, exactly as named): `vdd`, `vss`, `in`, `clk`, `out`
- **Parameters**:
  - `vth` (real, default 0.45): logic threshold in volts
  - `tedge` (real, default 100p): output transition time in seconds
- **Behavior**:
  - On the **rising edge** of `clk` (when `V(clk)` crosses `vth` upward), sample `V(in)` and hold it.
  - `V(out)` reflects the held value via `transition()`.
  - Between clock edges, `V(out)` remains constant.
- **Output**: use `transition()` — do NOT use `idt()`, `ddt()`, or `I() <+`.

## Testbench requirements

Create a minimal Spectre testbench that:
- Includes `sample_hold.va` via `ahdl_include`
- Provides vdd=0.9V, vss=0V
- Generates clock and varying input signal
- Saves signals: `in`, `clk`, `out`
- Runs transient for ~1us

## Deliverable

Two files:
1. `sample_hold.va` - the Verilog-A behavioral model
2. `tb_sample_hold.scs` - the Spectre testbench

Expected behavior:
- On each `clk` rising edge, `out` updates to the current `in` voltage.
- Between `clk` rising edges, `out` holds the last sampled value and does not
  continuously track `in`.
- Output transitions should be clean and bounded.
Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `IN`: input electrical
- `CLK`: input electrical
- `OUT`: output electrical

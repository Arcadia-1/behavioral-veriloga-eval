# Task: vbr1_l1_clocked_comparator:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Comparators and Decision Circuits
- Base function: Clocked comparator
- Domain: `voltage`
- Target artifact(s): `cmp_strongarm.va`, `tb_cmp_strongarm_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `cmp_strongarm.va`, `tb_cmp_strongarm_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `cmp_strongarm.va` declares module `cmp_strongarm` with positional ports: `CLK`, `VINN`, `VINP`, `DCMPN`, `DCMPP`, `LP`, `LM`, `VSS`, `VDD`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=4.25n maxstep=5p
```

The release harness expects these exact public scalar observables:

- `clk`
- `vinp`
- `vinn`
- `out_p`
- `out_n`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `gnd`
- `clk`
- `vinp`
- `vinn`

## Public Behavior Checks

- `outputs_toggle_nontrivially`
- `decision_samples_at_0p75_1p75_2p75_3p75ns_match_PPNN`

## Output Contract

Return exactly these source artifacts:

- `cmp_strongarm.va`
- `tb_cmp_strongarm_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `cmp_strongarm`.

# Task: cmp_strongarm_smoke

## Objective

Create a clocked StrongARM-style comparator behavioral model in Verilog-A and a minimal EVAS-compatible Spectre testbench.

## Specification

- **Module name**: `cmp_strongarm`
- **Ports** (all `electrical`, exactly as named): `clk`, `vinn`, `vinp`, `out_n`, `out_p`, `lp`, `lm`, `vss`, `vdd`
- **Behavior**:
  - Detect the rising edge of `clk`.
  - When `vinp > vinn`, drive `out_p` HIGH and `out_n` LOW.
  - When `vinp < vinn`, drive `out_p` LOW and `out_n` HIGH.
  - Outputs should show finite transitions and toggling when input polarity changes.

## Testbench requirements

Create a minimal Spectre testbench that:
- Includes `cmp_strongarm.va` via `ahdl_include`
- Provides VDD=0.9V, VSS=0V
- Generates a clock with ~500MHz frequency
- Creates differential input that changes polarity (vinp > vinn then vinp < vinn)
- Saves signals: `clk`, `vinp`, `vinn`, `out_p`, `out_n`
- Runs transient for ~4ns

## Deliverable

Two files:
1. `cmp_strongarm.va` - the Verilog-A behavioral model
2. `tb_cmp_strongarm.scs` - the Spectre testbench

Expected behavior:
- Output should toggle on each clock edge when input difference is sufficient
- Output should be valid after clock edge with some delay
Ports:
- `CLK`: input electrical
- `VINN`: input electrical
- `VINP`: input electrical
- `DCMPN`: output electrical
- `DCMPP`: output electrical
- `LP`: output electrical
- `LM`: output electrical
- `VSS`: inout electrical
- `VDD`: inout electrical

# Task: vbr1_l1_bang_bang_phase_detector:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: PLL / Clock / Event Timing
- Base function: Bang-bang phase detector
- Domain: `voltage`
- Target artifact(s): `bbpd_data_edge_alignment_ref.va`, `tb_bbpd_data_edge_alignment_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `bbpd_data_edge_alignment_ref.va`, `tb_bbpd_data_edge_alignment_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `bbpd_data_edge_alignment_ref.va` declares module `bbpd_data_edge_alignment_ref` with positional ports: `vdd`, `vss`, `clk`, `data`, `up`, `dn`, `retimed_data`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=170n maxstep=0.1n
```

The release harness expects these exact public scalar observables:

- `clk`
- `data`
- `up`
- `dn`
- `retimed_data`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `clk`
- `data`

## Public Behavior Checks

- `up_pulses_dominate_in_lead_window`
- `dn_pulses_dominate_in_lag_window`
- `up_dn_overlap_fraction_low`

## Output Contract

Return exactly these source artifacts:

- `bbpd_data_edge_alignment_ref.va`
- `tb_bbpd_data_edge_alignment_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a voltage-domain Alexander-style bang-bang phase detector (BBPD) that captures
near-edge data/clock alignment behavior.

Module name: `bbpd_data_edge_alignment_ref`.

Requirements:

1. Ports: `vdd`, `vss`, `clk`, `data`, `up`, `dn`, `retimed_data`
2. Use event-driven edge handling with EVAS-compatible `cross()`
3. Emit bounded UP/DN pulses according to data-edge alignment around the clock
4. Keep UP and DN mostly non-overlapping
5.  Stay in pure electrical voltage domain

Expected behavior:
- up pulse should fire when data edge leads clock edge
- dn pulse should fire when data edge lags clock edge
- up and dn should NOT overlap (overlap_frac < 2%)
- At least 6 data edges should generate up/dn pulses
Ports:
- `vdd`: electrical
- `vss`: electrical
- `clk`: electrical
- `data`: electrical
- `up`: electrical
- `dn`: electrical
- `retimed_data`: electrical (power rail)
- `vss`: inout electrical (power rail)
- `clk`: input electrical
- `data`: input electrical
- `up`: output electrical
- `dn`: output electrical
- `retimed_data`: output electrical

Implement this in Verilog-A behavioral modeling.

## Output Contract (MANDATORY)

- Return exactly two fenced code blocks:
  - first block: Verilog-A DUT (` ```verilog-a ... ``` `)
  - second block: Spectre testbench (` ```spectre ... ``` `)
- The Spectre testbench must include the DUT with `ahdl_include "<module>.va"`.
- Use a single `tran` analysis and include the required `save` signals for checker evaluation.

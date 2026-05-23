# Task: vbr1_l1_pfd_small_phase_error_response:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: PLL / Clock / Event Timing
- Base function: PFD small phase-error response
- Domain: `voltage`
- Target artifact(s): `pfd_updn.va`, `tb_pfd_small_phase_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `pfd_updn.va`, `tb_pfd_small_phase_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `pfd_updn.va` declares module `pfd_updn` with positional ports: `VDD`, `VSS`, `REF`, `DIV`, `UP`, `DN`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=300n maxstep=5p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `ref`
- `div`
- `up`
- `dn`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `ref`
- `div`

## Public Behavior Checks

- `short_up_pulses_present_for_small_phase_error`
- `up_dn_overlap_not_sustained`

## Output Contract

Return exactly these source artifacts:

- `pfd_updn.va`
- `tb_pfd_small_phase_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Create a phase-frequency detector behavioral model and matching transient
testbench focused on small REF/DIV phase-error response.

Module name: `pfd_updn`.

Required DUT behavior:

- Ports are exactly `VDD`, `VSS`, `REF`, `DIV`, `UP`, `DN`.
- Rising `REF` edges assert `UP`; rising `DIV` edges assert `DN`.
- When both internal states are high, reset both outputs to low.
- For small phase offsets, generate short bounded pulses without sustained
  `UP`/`DN` overlap.
- Drive output high as `V(VDD)` and low as `V(VSS)` through `transition()`.

Required testbench behavior:

- Include `pfd_updn.va` with `ahdl_include`.
- Generate `REF` and `DIV` clocks with small phase offsets.
- Save plain scalar observables `ref`, `div`, `up`, and `dn`.
- Run long enough to expose multiple small phase-error pulses.

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

# Task: pfd_small_phase_response_smoke

## Objective

Create a phase-frequency detector behavioral model in Verilog-A and a minimal EVAS-compatible Spectre testbench. The task focuses on small REF/DIV phase-error response: short, bounded UP/DN pulses should be visible without sustained overlap.

## Specification

- **Module name**: `pfd_updn`
- **Ports** (all `electrical`, exactly as named): `VDD`, `VSS`, `REF`, `DIV`, `UP`, `DN`
- **Parameters**:
  - `vth` (real, default `0.45`)
  - `tedge` (real, default `20p`)
- **Behavior**:
  - Rising edge of `ref` sets `up` high.
  - Rising edge of `div` sets `dn` high.
  - When both states are high, reset both to 0.
  - For small phase offsets, pulses should remain short and bounded with no sustained UP/DN overlap.
  - Output HIGH = V(vdd), LOW = V(vss) - read dynamically.

## Testbench requirements

Create a minimal Spectre testbench that:
- Includes `pfd_updn.va` via `ahdl_include`
- Provides vdd=0.9V, vss=0V
- Generates ref and div clocks with small phase offsets (~ps level)
- Saves signals: `ref`, `div`, `up`, `dn`
- Runs transient long enough to show several small phase-error UP/DN pulses

## Deliverable

Two files:
1. `pfd_updn.va` - the Verilog-A behavioral model
2. `tb_pfd_small_phase_ref.scs` - the Spectre testbench

Expected behavior:
- PFD should generate bounded pulses for small phase differences
- UP and DN should not remain high together after both input edges have arrived

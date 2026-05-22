# Task: vbr1_l1_xor_phase_detector:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: PLL / Clock / Event Timing
- Base function: XOR phase detector
- Domain: `voltage`
- Target artifact(s): `tb_xor_phase_detector_ref.scs`, `xor_phase_detector_ref.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `tb_xor_phase_detector_ref.scs`, `xor_phase_detector_ref.va`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `xor_phase_detector_ref.va` declares module `xor_phase_detector` with positional ports: `VDD`, `VSS`, `REF`, `DIV`, `PD_OUT`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=200n maxstep=100p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `ref`
- `div`
- `pd_out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `ref`
- `div`

## Public Behavior Checks

- `xor_pd_output_toggles`
- `xor_pd_duty_cycle_proportional_to_phase`

## Output Contract

Return exactly these source artifacts:

- `tb_xor_phase_detector_ref.scs`
- `xor_phase_detector_ref.va`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write a Verilog-A module named `xor_phase_detector`.

# Task: xor_pd_smoke

## Objective

Create an XOR Phase Detector behavioral model in Verilog-A and a minimal EVAS-compatible Spectre testbench.

## Specification

- **Module name**: `xor_phase_detector`
- **Ports** (all `electrical`, exactly as named): `vdd`, `vss`, `ref`, `div`, `pd_out`
- **Parameters**: `vth` (real, default 0.45), `tedge` (real, default 50p)
- **Behavior**:
  - `pd_out` is HIGH when `ref` and `div` are at **different** logic levels (XOR logic).
  - Updates on every edge of both `ref` and `div`.
  - Average `pd_out` duty cycle is proportional to phase difference.
  - Output HIGH = V(vdd), LOW = V(vss) - read dynamically.
- **Output**: use `transition()` only. No `idt`, `ddt`, or `I() <+`.

## Testbench requirements

Create a minimal Spectre testbench that:
- Includes `xor_phase_detector.va` via `ahdl_include`
- Provides vdd=0.9V, vss=0V
- Generates two clocks (ref and div) with phase offset
- Saves signals: `ref`, `div`, `pd_out`
- Runs transient for ~200ns

## Deliverable

Two files:
1. `xor_phase_detector.va` - the Verilog-A behavioral model
2. `tb_xor_phase_detector.scs` - the Spectre testbench

Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `REF`: input electrical
- `DIV`: input electrical
- `PD_OUT`: output electrical

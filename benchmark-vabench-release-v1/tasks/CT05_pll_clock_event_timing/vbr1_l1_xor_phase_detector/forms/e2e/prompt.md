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

Create an XOR phase detector behavioral model and matching transient testbench.

Artifact `xor_phase_detector_ref.va` must declare module `xor_phase_detector`.

Required DUT behavior:

- Ports are exactly `VDD`, `VSS`, `REF`, `DIV`, `PD_OUT`.
- `PD_OUT` is high when `REF` and `DIV` are at different logic levels and low
  when they match.
- Update output state on both rising and falling edges of `REF` and `DIV`.
- Drive output with `transition()` between the current supply rails.
- Do not use `idt()`, `ddt()`, or current contributions.

Required testbench behavior:

- Include `xor_phase_detector_ref.va` with `ahdl_include`.
- Generate two clocks with a fixed phase offset so `pd_out` has a measurable
  duty cycle rather than a stuck value.
- Save plain scalar observables `ref`, `div`, and `pd_out`.
- Run the public transient for about 200 ns.

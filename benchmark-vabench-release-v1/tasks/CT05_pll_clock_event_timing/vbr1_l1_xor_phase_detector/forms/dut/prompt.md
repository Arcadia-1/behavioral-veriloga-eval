# Task: vbr1_l1_xor_phase_detector:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: PLL / Clock / Event Timing
- Base function: XOR phase detector
- Domain: `voltage`
- Target artifact(s): `xor_phase_detector_ref.va`
- Supplied/reference support artifact(s): `tb_xor_phase_detector_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

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

## Public Behavior Checks

- `xor_logic_matches_ref_div`
- `xor_pd_output_toggles`
- `xor_pd_duty_cycle_proportional_to_phase`

## Output Contract

Return exactly one source artifact named `xor_phase_detector_ref.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# XOR phase detector DUT

Write the Verilog-A DUT artifact(s) for `XOR phase detector`.

This is a function-checked DUT task, not a generic companion wrapper. The
public contract below defines the exact module interface, voltage-domain
behavior, and waveform observables used by the release checker.

Domain: pure voltage-domain behavioral Verilog-A.

## Module Contract

- Declaration: `xor_phase_detector(vdd, vss, ref, div, pd_out)`

Ports:

- `vdd`, `vss`: electrical supply rails
- `ref`, `div`: input electrical clock waveforms
- `pd_out`: output electrical XOR phase-detector waveform

## Behavioral Contract

- `pd_out` is high exactly when `ref` and `div` are at different logic levels
- update on both input clock edges
- the average high fraction should reflect the phase offset in the companion testbench

## Public Evaluation Observables

The companion validation testbench saves these waveform columns:

- `ref`
- `div`
- `pd_out`

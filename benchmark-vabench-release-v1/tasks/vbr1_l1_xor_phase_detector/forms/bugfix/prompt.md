# Task: vbr1_l1_xor_phase_detector:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: PLL / Clock / Event Timing
- Base function: XOR phase detector
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`, `tb_xor_phase_detector_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `xor_phase_detector` with positional ports: `VDD`, `VSS`, `REF`, `DIV`, `PD_OUT`.
- `dut_fixed.va` declares module `xor_phase_detector` with positional ports: `VDD`, `VSS`, `REF`, `DIV`, `PD_OUT`.

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

- `output_high_when_inputs_differ`
- `output_low_when_inputs_match`
- `average_output_tracks_phase_difference`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# XOR phase detector Bugfix

Repair the supplied buggy Verilog-A implementation for `XOR phase detector`.

The fixed implementation must preserve the public module name and ports used by
the reference Spectre testbench. Domain: pure voltage-domain behavioral
Verilog-A. Do not use current contributions, transistor-level devices,
AC/noise analysis, or KCL/KVL solving assumptions.

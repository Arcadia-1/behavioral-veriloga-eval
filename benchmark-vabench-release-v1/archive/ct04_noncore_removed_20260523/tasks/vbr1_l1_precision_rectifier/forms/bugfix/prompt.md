# Task: vbr1_l1_precision_rectifier:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Precision rectifier
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`, `tb_precision_rectifier_buggy.scs`, `tb_precision_rectifier_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `precision_rectifier` with positional ports: `vin`, `vout`.
- `dut_fixed.va` declares module `precision_rectifier` with positional ports: `vin`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=120n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `vin`
- `vout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `negative_input_windows_drive_vout_near_zero`
- `positive_input_windows_follow_vin`
- `return_to_negative_window_clears_vout`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_precision_rectifier_bugfix

The provided voltage-domain precision rectifier has a negative-half-cycle bug:
negative input voltages are converted into positive output instead of being
blocked at zero. Fix the design so positive input voltages pass through and
negative input voltages drive the output near 0 V.

The fixed module must be named `precision_rectifier` and use electrical ports
`vin` and `vout`. Use the parameter `tr` for the output transition time.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.

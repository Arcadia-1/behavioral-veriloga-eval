# Task: vbr1_l1_voltage_clamp_or_limiter:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Voltage clamp or limiter
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`, `tb_voltage_clamp_buggy.scs`, `tb_voltage_clamp_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `voltage_clamp` with positional ports: `raw_level`, `vdd`, `vss`, `clamped_level`.
- `dut_fixed.va` declares module `voltage_clamp` with positional ports: `raw_level`, `vdd`, `vss`, `clamped_level`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=120n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `raw_level`
- `clamped_level`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `safe_window_low_inputs_clip_to_vlo`
- `safe_window_mid_inputs_follow_raw_level`
- `safe_window_high_inputs_clip_to_vhi`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_voltage_clamp_bugfix

The provided voltage-domain clamp model has a lower-bound clamp bug: input
levels below the configured low limit pass through instead of being clipped.
Fix the design so the output follows the raw input only inside the allowed
range, clips low inputs to the low limit, and clips high inputs to the high
limit.

The fixed module must be named `voltage_clamp` and use electrical ports
`raw_level`, `vdd`, `vss`, and `clamped_level`. Use the parameters `vlo`, `vhi`,
and `tr` for the low clamp, high clamp, and output transition time. The expected
default clamp range is 0.18 V to 0.72 V.

Use voltage contributions and smoothed output transitions. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.

# Task: vbr1_l1_first_order_lowpass:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Analog Behavioral Signal Conditioning
- Base function: First-order lowpass
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Supplied/reference support artifact(s): `dut_buggy.va`, `tb_first_order_lowpass_buggy.scs`, `tb_first_order_lowpass_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `dut_buggy.va` declares module `first_order_lowpass` with positional ports: `vin`, `vout`.
- `dut_fixed.va` declares module `first_order_lowpass` with positional ports: `vin`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=160n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `vin`
- `vout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `step_response_reaches_midscale_by_50ns`
- `step_response_is_monotonic_after_input_step`
- `late_output_settles_near_0p8v`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `dut_fixed.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_first_order_lowpass_bugfix

The provided voltage-domain first-order low-pass filter uses the wrong update
coefficient, so its step response settles much more slowly than the intended
time constant. Fix the model so each periodic update moves the output state
toward the input by the configured first-order coefficient.

The fixed module must be named `first_order_lowpass` and use electrical ports
`vin` and `vout`. It should initialize the filter state to zero, update the
state on a periodic timer, and drive `vout` as a smoothed voltage.

Use voltage contributions and event-driven state updates. Do not use current
contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `dut_fixed.va`.

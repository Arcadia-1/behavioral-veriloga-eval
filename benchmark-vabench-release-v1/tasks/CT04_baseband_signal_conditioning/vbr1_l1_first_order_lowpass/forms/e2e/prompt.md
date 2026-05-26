# Task: vbr1_l1_first_order_lowpass:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: First-order lowpass
- Domain: `voltage`
- Target artifact(s): `first_order_lowpass.va`, `tb_first_order_lowpass_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `first_order_lowpass.va`, `tb_first_order_lowpass_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `first_order_lowpass.va` declares module `first_order_lowpass` with positional ports: `vin`, `vout`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=160n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `vin`
- `vout`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vin`

## Public Behavior Checks

- `input_step_exercised`
- `monotone_first_order_step_response`
- `lagged_response_not_passthrough`
- `vout_reaches_expected_late_level`
- `bounded_without_overshoot`

## Output Contract

Return exactly these source artifacts:

- `first_order_lowpass.va`
- `tb_first_order_lowpass_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Write both the Verilog-A DUT and Spectre testbench for a timer-discretized first-order lowpass. This is the CT04 easy-anchor dynamic primitive: a single internal state, a step input, and a measurable settling trajectory.

The DUT module is `first_order_lowpass` with ports `vin, vout`. Both ports are electrical voltage nodes.

Required DUT behavior:
- Use a 500 ps timer update with state `y += 0.025 * (V(vin) - y)`.
- Drive `vout` from the internal state with `transition()`.
- The response must be monotone and visibly slower than an instantaneous copy.

Required testbench behavior:
- Apply a 0 to high step on `vin` and run long enough for the lowpass output to settle.
- Save `vin` and `vout` for fixed-time response checks.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

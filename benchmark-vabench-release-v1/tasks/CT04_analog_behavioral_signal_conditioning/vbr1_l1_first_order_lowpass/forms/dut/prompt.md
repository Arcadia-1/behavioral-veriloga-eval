# Task: vbr1_l1_first_order_lowpass:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: Analog Behavioral Signal Conditioning
- Base function: First-order lowpass
- Domain: `voltage`
- Target artifact(s): `first_order_lowpass.va`
- Supplied/reference support artifact(s): `tb_first_order_lowpass_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

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

## Public Behavior Checks

- `vout_monotone_step_response`
- `vout_not_instantaneous`
- `vout_reaches_expected_late_level`

## Output Contract

Return exactly one source artifact named `first_order_lowpass.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_first_order_lowpass_dut

Write a pure voltage-domain Verilog-A module for a timer-discretized first-order lowpass.

The DUT module is `first_order_lowpass` with ports `vin, vout`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Use a 500 ps timer update with state `y += 0.025 * (V(vin) - y)`.
- Drive `vout` from the internal state with `transition()`.
- The response must be monotone and visibly slower than an instantaneous copy.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `first_order_lowpass.va`.

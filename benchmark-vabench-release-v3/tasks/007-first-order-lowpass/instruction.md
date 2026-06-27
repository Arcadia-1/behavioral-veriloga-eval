# First Order Lowpass

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: First-order lowpass
- Domain: `voltage`
- Target artifact(s): `first_order_lowpass.va`
- Supplied/reference support artifact(s): `tb_first_order_lowpass_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `first_order_lowpass.va` declares module `first_order_lowpass` with positional ports: `vin`, `vout`.

## Public Scenario And Observable Contract

The supplied testbenches provide the exact stimulus and transient analysis
settings. The intended public scenario is a rising input step from about `0 V`
to about `0.8 V`, followed by a transient window long enough to observe
first-order settling.

The evaluator expects these exact public scalar observables:

- `vin`
- `vout`

## Public Behavior Checks

- `input_step_exercised`
- `monotone_first_order_step_response`
- `lagged_response_not_passthrough`
- `vout_reaches_expected_late_level`
- `bounded_without_overshoot`

## Output Contract

Return exactly one source artifact named `first_order_lowpass.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

Write a pure voltage-domain Verilog-A module for a timer-discretized first-order
lowpass: a single internal state, a step input, and a measurable settling
trajectory.

The DUT module is `first_order_lowpass` with ports `vin, vout`. Both ports are electrical voltage nodes.

Required behavior:
- Use a timer-updated internal real state to implement a stable finite-bandwidth
  first-order response with an effective time constant on the order of tens of
  nanoseconds for the supplied step stimulus.
- Drive `vout` from the internal state with `transition()`.
- The response must be monotone, bounded, and visibly slower than an
  instantaneous copy. Within several tens of nanoseconds after the step, `vout`
  should have crossed a substantial fraction of the final level; by the end of
  the transient window it should be close to the final input level.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

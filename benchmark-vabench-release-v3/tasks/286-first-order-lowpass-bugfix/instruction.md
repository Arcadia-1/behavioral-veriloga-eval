# First Order Lowpass Bugfix

One-shot bugfix task for a voltage-domain first-order low-pass filter.

## Agent-Visible Inputs

- `dut_buggy.va`
- `tb_first_order_lowpass_buggy.scs`
- `tb_first_order_lowpass_ref.scs`

## Required Output

- `dut_fixed.va`

## Public Interface

Preserve module `first_order_lowpass(vin, vout)` with electrical
voltage-domain ports.

## Public Scenario

The harness drives `vin` from about `0 V` to about `0.8 V` near `21 ns` and
observes a `160 ns` transient.

## Functional Contract

- `vout` should be a stable finite-bandwidth low-pass response with an
  effective time constant on the order of tens of nanoseconds.
- After the step, `vout` should move smoothly and monotonically toward `0.8 V`.
- `vout` should lag the input transition, not behave as a direct passthrough.
- Within several tens of nanoseconds, `vout` should cross a substantial
  fraction of the final level; by the end of the `160 ns` transient it should
  be close to `0.8 V`.
- The output should remain bounded and should not overshoot the input rail.

## Modeling Constraints

Use voltage-domain, event-driven Verilog-A and drive `vout` with voltage
contributions. Declare real state and helper quantities at module scope, not
inside `analog` or event blocks. Do not modify or emit support testbenches, add
checker logic, hard-code private waveform sample points, use current
contributions, `ddt()`, `idt()`, or `last_crossing()`.

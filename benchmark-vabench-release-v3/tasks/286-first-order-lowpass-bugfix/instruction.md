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

## Public Parameter And Bugfix Contract

The supplied buggy DUT exposes public parameters `alpha` and `tr`:

- `alpha = 0.010` in the buggy input: dimensionless recurrence coefficient.
  This value makes the supplied discrete-time response too slow for the public
  settling envelope and is the bug to repair if retaining the starter-style
  recurrence.
- `tr = 200 ps`: output transition smoothing time.

The visible source uses a timer-updated recurrence. The exact timer update
cadence and internal variable names are not the repair target by themselves;
the fixed artifact must instead produce the public finite-bandwidth response
shape below. If the fix keeps the same recurrence structure, increase the
effective recurrence gain to match a tens-of-nanoseconds time constant while
leaving legal parameter overrides meaningful.

## Public Scenario

The supplied testbenches drive `vin` from about `0 V` to about `0.8 V` and
observe the transient response through the settling window.

## Functional Contract

- `vout` should be a stable finite-bandwidth low-pass response with an
  effective time constant on the order of tens of nanoseconds.
- After the step, `vout` should move smoothly and monotonically toward `0.8 V`.
- `vout` should lag the input transition, not behave as a direct passthrough.
- Within several tens of nanoseconds, `vout` should cross a substantial
  fraction of the final level; by the end of the supplied transient it should
  be close to the final input level.
- The output should remain bounded and should not overshoot the input rail.

## Modeling Constraints

Use voltage-domain, event-driven Verilog-A and drive `vout` with voltage
contributions. Declare real state and helper quantities at module scope, not
inside `analog` or event blocks. Do not modify or emit support testbenches, add
checker logic, private test hooks, simulator-private side channels, hard-code private waveform sample points, use current
contributions, `ddt()`, `idt()`, or `last_crossing()`.

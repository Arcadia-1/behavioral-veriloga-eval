# First Order Lowpass Bugfix

## Task Contract
Repair the supplied buggy voltage-domain first-order low-pass DUT and return `dut_fixed.va`. This is a bugfix L1 task: preserve the public interface while correcting the response envelope.

## Public Verilog-A Interface
Preserve module `first_order_lowpass(vin, vout)` with scalar electrical voltage-domain ports. The visible starter and support decks are public inputs for understanding the bug and validation scenario.

## Public Parameter Contract
The supplied buggy DUT exposes `alpha` and `tr`:

- `alpha = 0.010`: dimensionless recurrence coefficient in the buggy starter; this makes the discrete-time response too slow if the starter recurrence is retained.
- `tr = 200 ps`: output transition smoothing time.

The starter uses a timer-updated recurrence. The exact internal variable names and update cadence are not the target by themselves; legal parameter overrides should remain meaningful.

## Required Behavior
The public validation step drives `vin` from about `0 V` to about `0.8 V` between 20 ns and 21 ns and observes `vout` through 160 ns. `vout` should move smoothly and monotonically toward the final level with a finite-bandwidth response on the order of tens of nanoseconds.

The required observable envelope is:

- At 30 ns, `vout` should still lag the input and remain below `0.45 V`.
- At 50 ns, `vout` should exceed `0.55 V`.
- At 90 ns, `vout` should exceed `0.70 V`.
- At 150 ns, `vout` should exceed `0.76 V`.
- From 22 ns onward, `vout` should remain bounded between about `-0.03 V` and `0.88 V`, should not overshoot the input rail, and should be monotonic across the 30/50/90/150 ns observation points except for small tail slack.

Implement the repair using any deterministic first-order low-pass structure that preserves legal public parameter overrides and satisfies this envelope; do not rely on particular internal variable names or a specific implementation template.

## Modeling Constraints
Use voltage-domain, event-driven Verilog-A and voltage contributions. Declare real state and helper quantities at module scope. Do not modify or emit support testbenches, add checker logic, hard-code testbench sample points, add simulator side channels, use current contributions, transistor-level devices, `ddt()`, `idt()`, or `last_crossing()`.

## Output Contract
Return exactly one source artifact named `dut_fixed.va`.

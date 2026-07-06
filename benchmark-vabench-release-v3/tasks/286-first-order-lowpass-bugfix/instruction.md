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
After an input step from about `0 V` to about `0.8 V`, `vout` should move smoothly and monotonically toward the final level with a finite-bandwidth response on the order of tens of nanoseconds. The output should lag the input rather than act as a direct passthrough, make substantial progress within several tens of nanoseconds, settle close to the final level by the end of the supplied transient, and remain bounded without overshoot.

## Modeling Constraints
Use voltage-domain, event-driven Verilog-A and voltage contributions. Declare real state and helper quantities at module scope. Do not modify or emit support testbenches, add checker logic, hard-code testbench sample points, add simulator side channels, use current contributions, transistor-level devices, `ddt()`, `idt()`, or `last_crossing()`.

## Output Contract
Return exactly one source artifact named `dut_fixed.va`.

# Debounce Latch

Implement a voltage-domain comparator decision debounce latch.

## Public Interface

Declare module `debounce_latch` with positional ports `sig, rst_n, out`. All
ports are electrical. `sig` is the noisy voltage-coded comparator decision,
`rst_n` is an active-low reset input, and `out` is the debounced decision
output.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: logic threshold for `sig` and `rst_n`.
- `vdd = 0.9 V`: logic high output level.
- `stable = 12n`: qualification time after a rising comparator-decision edge.
- `tr = 500p`: transition smoothing time for output changes.

## Functional Contract

- Initialize `out` low.
- When `rst_n` is below `vth`, force `out` low and cancel any pending
  qualification.
- When `sig` rises through `vth` while reset is released, start a qualification
  timer.
- When the qualification timer expires, set `out` high only if both `sig` and
  `rst_n` are still above `vth`.
- When `sig` falls below `vth`, clear `out` low and cancel any pending
  qualification.
- Hold the debounced output state between reset, input-edge, and timer events.

## Modeling Constraints

Return only `debounce_latch.va`. Use voltage contributions only. Do not modify
or emit the support testbench, add checker logic, hard-code waveform sample
points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`. For event-driven behavior, update local state in analog
event blocks and drive the output contribution outside those event blocks with
finite transition-style smoothing.

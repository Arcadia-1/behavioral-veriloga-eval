# PFD Timer Reset

Implement a voltage-domain phase-frequency detector with delayed mutual reset.

## Public Interface

Declare module `pfd_timer_reset` with positional ports `a, b, ub, d`. All ports
are electrical. Inputs `a` and `b` use voltage-coded logic.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: rising-edge threshold for inputs `a` and `b`.
- `vh = 0.9 V`: logic-high output level.
- `reset_delay = 100 ps from [0:inf)`: delay from the moment both detector
  sides have occurred to the mutual reset event.
- `tr = 10 ps from [0:inf)`: output transition time used for smooth
  voltage-domain output edges.

## Functional Contract

- A rising crossing of `a` through `vth` asserts the UP state.
- A rising crossing of `b` through `vth` asserts the DOWN state.
- Output `ub` is active-low: drive it near `0 V` while the UP state is asserted
  and near `vh` otherwise.
- Output `d` is active-high: drive it near `vh` while the DOWN state is asserted
  and near `0 V` otherwise.
- When both sides have occurred, schedule a timer reset after `reset_delay` and
  clear both states at that timer event.
- Output transitions should use smooth voltage-domain transitions with the
  public transition time `tr`.

## Modeling Constraints

Return only `pfd_timer_reset.va`. Use voltage contributions only. Do not modify
or emit the support testbench, add checker logic, hard-code private waveform
sample points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`.

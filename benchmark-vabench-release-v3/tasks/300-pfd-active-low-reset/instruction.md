# PFD Active Low Reset

Implement a voltage-domain phase-frequency detector with active-low UP and
delayed mutual reset.

## Public Interface

Declare module `pfd_active_low_reset` with positional ports `ref, fb, upb,
down`. All ports are electrical. Inputs `ref` and `fb` use voltage-coded logic.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: rising-edge threshold for inputs `ref` and `fb`.
- `vh = 0.9 V`: logic-high output level.
- `reset_delay = 80 ps from [0:inf)`: delay from the moment both detector
  sides have occurred to the mutual reset event.
- `tr = 10 ps from [0:inf)`: output transition time used for smooth
  voltage-domain output edges.

## Functional Contract

- A rising crossing of `ref` through `vth` asserts the UP state.
- A rising crossing of `fb` through `vth` asserts the DOWN state.
- Output `upb` is active-low: drive it near `0 V` while the UP state is asserted
  and near `vh` otherwise.
- Output `down` is active-high: drive it near `vh` while the DOWN state is
  asserted and near `0 V` otherwise.
- When both sides have occurred, schedule a timer reset after `reset_delay` and
  clear both states at that timer event.
- Output transitions should use smooth voltage-domain transitions with the
  public transition time `tr`.

## Modeling Constraints

Return only `pfd_active_low_reset.va`. Use voltage contributions only. Do not
modify or emit the support testbench, add checker logic, hard-code private
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`.

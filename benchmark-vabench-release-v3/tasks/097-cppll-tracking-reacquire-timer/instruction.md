# CPPLL Tracking Reacquire Timer

Implement `cppll_timer_ref.va` in Verilog-A.

## Public Interface

Declare module `cppll_timer_ref(VDD, VSS, ref_clk, fb_clk, dco_clk,
vctrl_mon, lock)` with scalar electrical voltage-domain ports. `VDD` and `VSS`
are supply rails, `ref_clk` is the reference clock input, and `fb_clk`,
`dco_clk`, `vctrl_mon`, and `lock` are outputs.

## Public Parameter Contract

- `div_ratio`: feedback divider ratio, default `8`, positive integer.
- `f_center`: nominal DCO center frequency in Hz, default `800.0e6`.
- `kvco_hz_per_v`: DCO gain in Hz/V, default `350.0e6`.
- `f_min`, `f_max`: DCO frequency clamp limits, defaults `300.0e6` and
  `1.6e9`.
- `kp`, `ki`: proportional and integral phase-control gains, defaults `8.0e6`
  and `1.2e5`.
- `integ_min`, `integ_max`: integral clamp limits, defaults `-0.45` and
  `0.45`.
- `vctrl_init`: initial control voltage, default `0.45`.
- `tedge`: output transition smoothing time, default `20p`.
- `lock_tol`: phase-error tolerance for lock detection, default `0.4e-9`.
- `lock_count_target`: consecutive in-tolerance reference edges required for
  lock, default `6`.

## Functional Contract

- Initialize the DCO, feedback divider, loop state, and lock state
  deterministically.
- Measure reference-edge timing against feedback-edge timing and wrap phase
  error into the current reference period when possible.
- Update a bounded PI-like control voltage and clamp it to the supply range.
- Generate a DCO clock whose frequency follows the bounded control voltage and
  stays within `f_min` and `f_max`.
- Toggle `fb_clk` from the divided DCO clock according to `div_ratio`.
- Assert `lock` only after enough consecutive reference edges have phase error
  within `lock_tol`.
- Drive digital-like outputs relative to `VDD` and `VSS`; drive `vctrl_mon` as
  the analog control monitor.

## Modeling Constraints

Return only `cppll_timer_ref.va`; companion files used by the validation
scenario are supplied separately. Do not emit a Spectre testbench, checker
logic, private test hooks, or simulator-private side channels. Use
voltage-domain, event-driven Verilog-A; do not use transistor-level devices,
current contributions, `ddt()`, or `idt()`.

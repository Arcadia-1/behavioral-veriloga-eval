# Offset Bisection Driver

Implement a comparator-offset bisection stimulus driver with an explicit
common-mode input.

## Public Interface

Declare module `offset_bisection_driver` with positional ports `clk, vout, vcm,
vinp, vinn`. All ports are electrical. `clk` is the update clock, `vout` is the
comparator decision input, `vcm` is the analog common-mode reference, and
`vinp`/`vinn` are the generated differential stimulus outputs.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: logic threshold used for `clk` and `vout`.
- `step_initial = 10m V`: initial differential bisection step.

## Functional Contract

- Initialize the signed differential search value to zero and start with
  `step_initial`.
- On each falling crossing of `clk` through `vth`, sample `vout` against
  `vth`.
- A sampled low decision should increase `vinp - vinn`; a sampled high decision
  should decrease `vinp - vinn`.
- Halve the bisection step only when the sampled comparator polarity changes
  from the previous update.
- Drive `vinp = vcm + diff/2` and `vinn = vcm - diff/2`, where `diff` is the
  current signed search value.
- Hold the generated stimulus between update events.

## Modeling Constraints

Return only `offset_bisection_driver.va`. Use voltage contributions only. Do
not modify or emit the support testbench, add checker logic, hard-code waveform
sample points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`. Update bisection state in analog event blocks and drive
voltage outputs outside those event blocks.

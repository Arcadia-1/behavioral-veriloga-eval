# Strongarm Style Latch Comparator

Implement a voltage-domain StrongARM-style clocked latch comparator.

## Public Interface

Declare module `cmp_strongarm` with positional ports `CLK, VINN, VINP, DCMPN,
DCMPP, LP, LM, VSS, VDD`. All ports are electrical. `CLK` is the comparator
clock, `VINP` and `VINN` are the differential inputs, `DCMPP` and `DCMPN` are
the complementary decision outputs, `LP` and `LM` are latch-state monitor
outputs, and `VSS`/`VDD` are supply rails.

## Public Parameter Contract

Provide these overrideable public parameters:

- `td_cmp = 0`: comparator output delay.
- `voffset = 0`: input-referred offset subtracted from `VINP - VINN`.

## Functional Contract

- Initialize all public decision and latch-state outputs low.
- Use `V(VDD,VSS)/2` as the clock decision threshold.
- On each rising clock crossing, latch the sign of
  `V(VINP,VSS) - V(VINN,VSS) - voffset`.
- For a positive latched differential input, drive `DCMPP` and `LP` high while
  `DCMPN` and `LM` remain low. For a negative latched differential input, drive
  `DCMPN` and `LM` high while `DCMPP` and `LP` remain low.
- For an exactly zero effective differential input, keep both complementary
  decision states low.
- On each falling clock crossing, reset all public decision and latch-state
  outputs low.
- Hold the latched decision between clock events; the model must not become
  transparent while the clock is high.

## Modeling Constraints

Return only `cmp_strongarm.va`. Use voltage contributions only. Do not modify
or emit the support testbench, add checker logic, hard-code waveform sample
points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`. For Cadence-style event modeling, update discrete state in
`cross()`/`initial_step` event blocks and drive smoothed output contributions
outside those event blocks.

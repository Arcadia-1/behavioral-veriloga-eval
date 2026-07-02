# Hysteresis Comparator

Implement a voltage-domain differential comparator with hysteresis.

## Public Interface

Declare module `cmp_hysteresis` with positional ports `VINN, VINP, OUTN, OUTP,
VSS, VDD`. All ports are electrical. `VINP` and `VINN` are the differential
inputs, `OUTP` and `OUTN` are complementary decision outputs, and `VSS`/`VDD`
are supply rails.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vhys = 10m V`: total hysteresis width.
- `tedge = 50p`: transition smoothing time for the complementary outputs.

## Functional Contract

- Initialize `OUTP` high only when `V(VINP,VSS) - V(VINN,VSS)` is above
  `+vhys/2`; otherwise initialize `OUTP` low and `OUTN` high.
- Switch to the high `OUTP` state only when the differential input rises
  through `+vhys/2`.
- Switch back to the low `OUTP` state only when the differential input falls
  through `-vhys/2`.
- Hold the previous decision while the differential input remains inside the
  hysteresis band.
- Drive `OUTP` and `OUTN` as complementary rail-referenced outputs using finite
  transition-style smoothing.

## Modeling Constraints

Return only `cmp_hysteresis.va`. Use voltage contributions only. Do not modify
or emit the support testbench, add checker logic, hard-code waveform sample
points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`. For event-driven hysteresis, update a retained local state
at threshold crossings and keep output contributions outside the event blocks.

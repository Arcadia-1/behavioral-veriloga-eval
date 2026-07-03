# Threshold Comparator

Implement a voltage-domain single-ended threshold comparator.

## Public Interface

Declare module `comparator` with positional ports `VDD, VSS, VINP, VINN,
OUT_P`. All ports are electrical. `VDD` and `VSS` are supply rails, `VINP` and
`VINN` are the differential inputs, and `OUT_P` is the single-ended decision
output.

## Public Parameter Contract

Provide this overrideable public parameter:

- `tedge = 100p`: transition smoothing time for `OUT_P`.

## Functional Contract

- Initialize `OUT_P` from the initial sign of `V(VINP,VSS) - V(VINN,VSS)`.
- Drive `OUT_P` high to `VDD` when `VINP` crosses above `VINN`.
- Drive `OUT_P` low to `VSS` when `VINP` crosses below `VINN`.
- Respond to both rising and falling zero-differential crossings.
- Use finite transition-style smoothing for rail-referenced output changes.

## Modeling Constraints

Return only `comparator.va`. Use voltage contributions only. Do not modify or
emit the support testbench, add checker logic, hard-code waveform sample
points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`. Update the retained decision state at crossing events and
drive the output contribution outside those event blocks.

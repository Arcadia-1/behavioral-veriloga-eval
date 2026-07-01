# Flash 8-Level Sum With One-Cycle Delay

Implement a differential 8-level flash threshold summarizer with one-cycle
delay.

## Public Interface

Declare module `flash_8level_sum_delay` with positional ports `vip, vim,
clks, reset, refp, refn, doutsum, doutsumdelay`. All ports are electrical.
The `reset` port is present for interface compatibility; this task does not
require it to change the sampled state.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: rising-edge threshold for `clks`.
- `ref_scaling = 0.5`: scale factor applied to the differential reference span
  before forming flash thresholds.
- `tt = 10 ps`: output transition smoothing time.

## Functional Contract

On each rising `clks` edge, compare the differential input `V(vip)-V(vim)`
against eight symmetric flash thresholds derived from `V(refp)-V(refn)`. The
threshold magnitudes are the odd eighths of the scaled reference span:
`1/8`, `3/8`, `5/8`, and `7/8`, with both positive and negative polarities.

Drive `doutsum` with the current threshold count normalized by eight. Drive
`doutsumdelay` with the previous sampled normalized count, so it represents a
one-cycle delayed flash summary.

## Modeling Constraints

Return only `flash_8level_sum_delay.va`. Use deterministic voltage-domain
Verilog-A and smooth output transitions. Do not modify or emit the support
testbench, add checker logic, hard-code private waveform sample points, add
simulator-private side channels, use current contributions, `ddt()`, or
`idt()`.

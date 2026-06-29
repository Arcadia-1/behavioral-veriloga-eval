# Smooth Tanh Comparator

Implement a pure voltage-domain smooth comparator macro with a fixed default
tanh transfer.

## Public Interface

Declare module `smooth_tanh_comparator` with positional ports `sigin, sigref,
sigout`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `sigout_high = 1.0 V`: upper output level; use a finite real voltage.
- `sigout_low = -1.0 V`: lower output level; use a finite real voltage.
- `sigin_offset = 0.05 V`: input-referred offset applied to `V(sigin,sigref)`.
- `comp_slope = 4.0 1/V`: nonnegative tanh slope coefficient.

## Functional Contract

Drive `sigout` according to:

```text
0.5 * (sigout_high - sigout_low)
    * tanh(comp_slope * (V(sigin,sigref) - sigin_offset))
    + 0.5 * (sigout_high + sigout_low)
```

The default transfer ranges from `-1 V` to `+1 V`, crosses near
`V(sigin,sigref) = 0.05 V`, and remains smooth rather than hard-switching.

## Modeling Constraints

Return only `smooth_tanh_comparator.va`. Use voltage contributions only. Do not
modify or emit the support testbench, add checker logic, hard-code private
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`.

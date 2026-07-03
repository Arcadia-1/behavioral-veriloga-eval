# Smooth Comparator Tanh

Implement a pure voltage-domain smooth comparator based on a tanh transfer.

## Public Interface

Declare module `smooth_comparator_tanh` with positional ports `sigin, sigref,
sigout`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `high = 1.0 V`: upper output level.
- `low = -1.0 V`: lower output level.
- `offset = 0.0 V`: input-referred offset applied to `V(sigin,sigref)`.
- `comp_slope = 1000.0 1/V`: tanh slope coefficient.

## Functional Contract

Drive `sigout` according to this public transfer:

```text
0.5 * (high - low) * tanh(comp_slope * (V(sigin,sigref) - offset))
    + 0.5 * (high + low)
```

The output should move smoothly between `low` and `high` as `sigin` crosses
`sigref + offset`; it should not hard-switch like an ideal threshold
comparator.

## Modeling Constraints

Return only `smooth_comparator_tanh.va`. Use voltage contributions only. Do not
modify or emit the support testbench, add checker logic, hard-code waveform
sample points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`.

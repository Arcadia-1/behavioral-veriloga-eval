# Cyclic Decoder 10b Audit

- Gate 1: kept as an independent cyclic ADC decision decoder. It is distinct from SAR serial decoding because cyclic decisions can contribute full, half, or zero weight at each ready pulse.
- Public contract: sample `dp/dn` on rising `ready`, accumulate descending `nbit` weights with full/half/zero semantics, publish a centered normalized code on rising `clks`, then reset.
- Cadence reference correspondence: the local ADC reference shows decision-to-code conversion; this benchmark captures the cyclic ADC-specific ternary weighting convention.
- Duplicate review: distinct from retained weighted DAC/decoder rows because the code is built sequentially from comparator decisions and includes half-weight cyclic states.
- Evaluation note: hidden coverage should include a different ready/decision pattern, including half-weight `dn` contributions, and checker expectations should be derived from saved events.

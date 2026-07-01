# SAR 5-Bit Serial Decoder Audit

- Gate 1: kept as an independent SAR readout component. It evaluates ready-pulsed serial comparator decisions and conversion-clock publication, which is distinct from the retained weighted DAC/decoder rows.
- Public contract: sample one decision per rising `ready` edge, assign descending 5-bit SAR weights from MSB to LSB, publish a centered normalized code on rising `clks`, then reset for the next conversion.
- Cadence reference correspondence: the local Cadence ADC reference illustrates code generation from analog/digital decisions; this benchmark narrows that pattern to SAR serial decision accumulation and clocked publication.
- Duplicate review: distinct from `193-cyclic-decoder-10b` because SAR decisions are binary full-weight decisions, while the cyclic decoder has full/half/zero ternary weighting.
- Evaluation note: hidden coverage should include a different decision sequence from the visible smoke scenario, and checker expectations should be derived from saved `ready`, `din`, and `clks` events.

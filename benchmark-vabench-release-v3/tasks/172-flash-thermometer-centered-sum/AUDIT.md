# Centered Flash-Code Summary Audit

- Gate 1: kept as an independent data-converter component after human review because it is a centered flash-code summarizer, not just an uncentered thermometer fraction counter.
- Public contract: count eight scalar thermometer taps above `vth`, center the code at four asserted taps, and scale each tap difference by `gain`.
- Cadence reference correspondence: the local Cadence thermometer-bus article uses thresholded digital-voltage taps to represent thermometer-coded data; this benchmark evaluates the complementary post-processing summary of those taps.
- Duplicate review: distinct from the retained flash threshold/residue tasks because this row exposes continuous centered-code summarization rather than clocked residue generation or selected threshold tap generation.
- Evaluation note: hidden coverage should be materially distinct from the visible smoke scenario, and checker expectations should be derived from saved input taps rather than from one fixed waveform table.

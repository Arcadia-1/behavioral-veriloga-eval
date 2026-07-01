# Coarse QTZ 3bit Residue Audit

- Gate 1: kept as an independent coarse quantizer/residue component. It is distinct from ideal ADC rows because it exposes both binary coarse code and analog quantization residue.
- Public contract: clip input to `[-vref, +vref]`, quantize to eight round-to-nearest codes with endpoint saturation, drive LSB-to-MSB binary outputs, and report clipped-input minus quantized-level residue.
- Cadence reference correspondence: the local ADC reference illustrates ideal ADC code generation; this benchmark adds explicit clipping and residue reporting, which are the functional parts under review.
- Duplicate review: distinct from retained ideal ADC/DAC rows because the residue output is part of the circuit function, not only a code or voltage reconstruction.
- Evaluation note: hidden coverage should include endpoint clipping and interior codes, and checker expectations should be derived from saved `vin` samples.

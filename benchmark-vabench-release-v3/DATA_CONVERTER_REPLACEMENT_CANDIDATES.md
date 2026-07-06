# Data Converter Replacement Candidates

This note records data-converter candidates that should be reviewed as
replacement or backfill material for the original `001`-`300` benchmark
surface, not as additional final benchmark numbers after `300`.

Issue #109 accepted six materialized candidates and one fresh replacement into
the original full-300 surface at `052`-`057` and `075`. The previous
`500-deterministic-mismatch-dac6` candidate was retired after duplicate review
because it was too close to the existing mismatch-DAC coverage. The old
temporary data-converter `495`-`501` task ids are no longer active
data-converter benchmark rows; they are referenced below only as provenance for
the re-slot mapping. The current `495`-`501` task ids are now separate
issue #109 bias/reference/power-management and measurement replacements.

## Current Closure Status

As of the issue #109 re-slot, `TASKS.json` contains 91 data-converter-category
rows when `data_converter` and `data_converter_models` are counted together.
Six formerly temporary candidates plus the new correlated-double-sampler row are
now active replacement rows inside the original `001`-`300` surface at
`052`-`057` and `075`; no active data-converter `495`-`501` task directories
remain, even though those numeric ids now host non-converter issue #109
replacement rows.

The 2026-07-02 closeout EVAS sweep over the pre-slot candidate pool reported
`88/88` gold pass and `326/326` negative variants rejected. After the 056
replacement, fresh issue #109 validation on the seven active rows passes EVAS
visible and hidden sweeps (`7/7` gold PASS and `35/35` negatives rejected for
each split), Spectre hidden gold (`7/7` PASS), and Spectre hidden negatives
(`35/35` rejected). The changed visible Spectre surface also passes gold for
`053`, `054`, `056`, and `075` and rejects their `20/20` visible negative
variants.

Rows `096`, `105`, `283`, and `075` should be treated as L2 data-converter
tasks: `096` and `075` are measurement/support flows, `105` is a pipeline ADC
residue-chain flow, and `283` is an end-to-end SAR ADC/DAC loop. That L2 label
does not by itself assign final scoring slots; final replacement, removal, and
counting decisions remain upstream review decisions.

## Replacement Policy

- Do not grow the scored benchmark simply by appending `301+` rows.
- Use these candidates to replace rows that are hard duplicates, weak parameter
  variants, or rows whose behavior is better represented by a more distinct
  Cadence-backed converter function.
- Keep final numbering, removal policy, and counted status as upstream review
  decisions.
- Keep Cadence-derived implementation details in the task assets only when they
  are part of the public circuit contract. The public prompt should describe
  observable converter behavior rather than copying private reference code.

## Accepted Re-slot Mapping

| Former temporary row | Active replacement row | Candidate function | Why it is distinct | Current decision |
| --- | --- | --- | --- | --- |
| `498-dc-aware-adc3bit` | `052-dc-aware-adc3bit` | Static three-bit ADC whose output is valid without a sampling clock | Separates combinational/DC-compatible conversion from clocked transient ADC rows | Accepted as an L1 data-converter replacement |
| `499-latched-bus-dac8` | `053-latched-bus-dac8` | Parallel DAC that latches an input bus on update-clock edges and holds between updates | Adds update-strobe and hold behavior missing from transparent binary DAC rows | Accepted as an L1 data-converter replacement |
| `497-thermometer-bus-encoder` | `054-thermometer-bus-encoder` | Analog input to thermometer-prefix output bus | Models a reusable thermometer-bus source/encoder instead of decoding or summarizing an existing bus | Accepted as an L1 data-converter replacement |
| `495-slew-rate-dac4` | `055-slew-rate-dac4` | Four-bit DAC with finite `slew()` output motion | Output slew rate is part of the converter macro behavior, not only a cosmetic `transition()` edge | Accepted as an L1 data-converter replacement |
| Retired: `500-deterministic-mismatch-dac6` | `056-correlated-double-sampler` | Two-phase correlated double sampler that subtracts a stored reset level from a later signal sample | Adds ADC/front-end reset/signal correction behavior absent from simple sample-hold and ADC/DAC rows; avoids duplicating mismatch-DAC coverage from `027` | Accepted as an L1 data-converter-front-end replacement |
| `496-first-order-sigma-delta-modulator` | `057-first-order-sigma-delta-modulator` | First-order sigma-delta modulator with one-bit feedback stream | Adds a converter architecture absent from the SAR/flash/weighted-DAC families | Accepted as an L1 data-converter replacement |
| `501-adc-static-linearity-monitor` | `075-adc-static-linearity-monitor` | Sampled monitor that accumulates maximum ADC static code error over a sweep | Adds measurement-flow coverage rather than another converter core | Accepted as an L2 measurement replacement |

## Additional Candidates To Materialize After Slot Review

| Candidate function | Cadence-backed modeling pattern | Why it may improve the benchmark | Suggested replacement use | Main risk before implementation |
| --- | --- | --- | --- | --- |
| Generated-bit ADC quantizer | Generated repeated bit outputs, explicit MSB/LSB order, threshold update | Covers ADC bus generation and bit ordering more strongly than scalar ideal ADC rows | Replace one duplicated ideal ADC output-bus row | Needs careful prompt wording so `generate` style is not a hidden implementation requirement |
| Table-driven converter transfer | Data-file backed code/level mapping with interpolation or clamping | Useful if the benchmark wants calibrated converter behavior from a public table artifact | Candidate replacement only after table-file support policy is settled | `$table_model` and file dependency support may place it in extension/non-scored scope first |

## Non-Candidates Or Deferred Forms

- The Virtuoso PCell / variable-width symbol machinery from Cadence guidance is
  useful design context, but it is not itself a vaBench DUT target.
- Random or Monte Carlo converter variation should not become a deterministic
  scored row unless the seed, distribution, and instance semantics are fully
  public and simulator-aligned.
- Pure language-extension coverage remains in the `301+` extension layer. A
  row should enter the full-300 replacement pool only when the circuit function
  is independently useful, not merely because it exercises a Verilog-A feature.

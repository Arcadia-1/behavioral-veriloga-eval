# Data Converter Replacement Candidates

This note records data-converter candidates that should be reviewed as
replacement or backfill material for the original `001`-`300` benchmark
surface, not as additional final benchmark numbers after `300`.

The current `495`-`501` rows are materialized review candidates only. Their
temporary IDs make the assets executable in the repository, but they should not
be interpreted as final scored benchmark numbering. If upstream accepts one of
these rows as benchmark content, it should be assigned to a replacement slot
inside the original full-300 surface, or explicitly kept outside the scored
denominator.

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

## Materialized Candidates

| Temporary row | Candidate function | Why it is distinct | Suggested replacement use | Open decision |
| --- | --- | --- | --- | --- |
| `495-slew-rate-dac4` | Four-bit DAC with finite `slew()` output motion | Output slew rate is part of the converter macro behavior, not only a cosmetic `transition()` edge | Replace an ideal binary/restore DAC variant if upstream wants one DAC row to cover finite output slew | Whether this is sufficiently converter-specific or should remain an operator-support row |
| `496-first-order-sigma-delta-modulator` | First-order sigma-delta modulator with one-bit feedback stream | Adds a converter architecture absent from the SAR/flash/weighted-DAC families | High-priority replacement/backfill for a duplicate weighted-DAC or simple ideal-ADC row | Exact L1 vs small L2 label; it is a loop, but the target is one reusable modulator DUT |
| `497-thermometer-bus-encoder` | Analog input to thermometer-prefix output bus | Models a reusable thermometer-bus source/encoder instead of decoding or summarizing an existing bus | Replace a simple thermometer helper only if upstream counts source/support components as benchmark rows | L1 support component vs standalone converter-interface function |
| `498-dc-aware-adc3bit` | Static three-bit ADC whose output is valid without a sampling clock | Separates combinational/DC-compatible conversion from clocked transient ADC rows | Replace or upgrade an ideal ADC row that differs mostly by bit count or rail choice | Whether the benchmark wants an explicitly static ADC row in the scored set |
| `499-latched-bus-dac8` | Parallel DAC that latches an input bus on update-clock edges and holds between updates | Adds update-strobe and hold behavior missing from transparent binary DAC rows | Replace a repeated binary DAC or restore-DAC variant if clocked bus update is preferred | Whether this should replace an existing clocked DAC rather than add another DAC family row |
| `500-deterministic-mismatch-dac6` | Binary DAC with public deterministic element-weight errors and actual-weight normalization | Models calibration/mismatch behavior without random or hidden coefficients | Upgrade or replace a weak mismatch/weighted-DAC row | Exact mismatch values are public circuit parameters, not private checker data |
| `501-adc-static-linearity-monitor` | Sampled monitor that accumulates maximum ADC static code error over a sweep | Adds measurement-flow coverage rather than another converter core | Replace or upgrade a weak static-linearity/measurement row | L2 measurement/support label and final counting policy |

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

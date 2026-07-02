# Data Converter Replacement Candidates

This note records data-converter candidates that should be reviewed as
replacement or backfill material for the original `001`-`300` benchmark
surface, not as additional final benchmark numbers after `300`.

The current `495`-`497` rows are materialized review candidates only. Their
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

## Additional Candidates To Materialize After Slot Review

| Candidate function | Cadence-backed modeling pattern | Why it may improve the benchmark | Suggested replacement use | Main risk before implementation |
| --- | --- | --- | --- | --- |
| DC-compatible ideal ADC | Combinational A2D conversion that also behaves under DC-style operating analyses | Distinct from clocked transient ADC rows; useful when the benchmark wants analysis-aware converter models | Replace or upgrade one ideal ADC row that currently differs mostly by bit count or rail choice | EVAS and current v3 harness are transient-oriented; may need a transient-compatible public test or remain non-scored |
| Fixed-width scalable-style DAC | Thresholded voltage bus, looped bit accumulation, clocked update, fixed public width | Captures scalable bus/generator style without relying on Virtuoso variable-width symbol/PCell machinery | Replace a repeated binary DAC or restore-DAC variant if the loop/bus contract is considered valuable | Must avoid making "same DAC with different implementation style" the only novelty |
| Deterministic ladder/mismatch DAC | Structural or structured weighted ladder with deterministic element mismatch | Strengthens the DAC mismatch family with a more circuit-recognizable ladder abstraction | Upgrade/replace the existing mismatch DAC row rather than add a near duplicate | Must stay in the supported voltage-domain subset and avoid current-domain KCL/MNA claims unless deliberately scoped |
| Generated-bit ADC quantizer | Generated repeated bit outputs, explicit MSB/LSB order, threshold update | Covers ADC bus generation and bit ordering more strongly than scalar ideal ADC rows | Replace one duplicated ideal ADC output-bus row | Needs careful prompt wording so `generate` style is not a hidden implementation requirement |
| Static linearity measurement flow | Code sweep, endpoint/gain extraction, and INL/DNL-style measurement | More valuable as a converter L2 measurement row than another component variant | Upgrade `096-converter-static-linearity-measurement` or replace a weak measurement flow | Must keep testbench vs DUT boundary explicit and avoid hard-coding hidden checker samples |
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

# v3 Audit: Slew Output Reset Recovery

## Gate 1

- Counting label: `cadence_boundary_only`.
- Rationale: this row primarily exercises the Verilog-A `slew()` operator across reset and recovery events. It is useful compatibility coverage and a reusable support idiom, but as written it should not be counted as an independent core circuit-function benchmark.

## Gate 2

- Public prompt uses the mandatory vaBench v3 instruction sections and avoids private evaluation-mechanism wording.
- Public contract treats `fall_rate` as a positive falling-slope magnitude while requiring Cadence-compatible `slew(target, rise_rate, -fall_rate)` usage.
- Gold and concrete negatives use the negative third `slew()` argument required by Cadence Verilog-A semantics.

Certification status: targeted validation completed after the `slew()` sign repair. EVAS2 reference implementation passed; EVAS2 negative variants were rejected. Spectre reference implementation passed; Spectre negative variants were rejected. The only Spectre warning observed was environment-level `VACOMP-2435` for deprecated `CDS_AHDLCMI_ENABLE`, not a model warning.

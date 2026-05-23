# vaBench Release Dual Rerun Import

Date: 2026-05-24

This report records whether fresh release EVAS/Spectre rerun results
were imported into release evidence. It does not import blocked, dry-run,
or still-running summaries.

## Summary

| Metric | Value |
| --- | ---: |
| status | `partial_imported` |
| stale summary | `True` |
| summary tasks total | 37 |
| current queue count | 0 |
| imported primary results | 35 |
| skipped results | 0 |
| imported pass | 35 |
| imported fail | 0 |

Reason: Stale-count dual rerun summary was partially imported by exact entry/form match; unmatched rows remain skipped and missing rows remain pending.

## Notes

- Only primary gold/fixed pass bundles are imported into the release denominator.
- Bugfix buggy companion bundles remain separate badcase evidence and are not scored here.
- Partial stale-count import is conservative: it imports only exact current release entry/form matches.

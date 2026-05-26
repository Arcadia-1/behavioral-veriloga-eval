# vaBench Release Dual Rerun Import

Date: 2026-05-26

This report records whether fresh release EVAS/Spectre rerun results
were imported into release evidence. It does not import blocked, dry-run,
or still-running summaries.

## Summary

| Metric | Value |
| --- | ---: |
| status | `imported` |
| stale summary | `False` |
| summary tasks total | 2 |
| current queue count | 2 |
| imported primary results | 2 |
| skipped results | 0 |
| imported pass | 0 |
| imported pending | 2 |
| imported fail | 0 |

Reason: Fresh dual rerun imported with external pending blockers; release certification remains pending.

## Notes

- Only primary gold/fixed pass bundles are imported into the release denominator.
- Bugfix buggy companion bundles remain separate badcase evidence and are not scored here.
- Partial stale-count import is conservative: it imports only exact current release entry/form matches.

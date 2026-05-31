# vaBench Release Dual Rerun Import

Date: 2026-05-27

This report records whether fresh release EVAS/Spectre rerun results
were imported into release evidence. It does not import blocked, dry-run,
or still-running summaries.

## Summary

| Metric | Value |
| --- | ---: |
| status | `imported` |
| stale summary | `False` |
| summary tasks total | 54 |
| current queue count | 54 |
| imported primary results | 54 |
| skipped results | 0 |
| imported pass | 54 |
| imported pending | 0 |
| imported fail | 0 |

Reason: Fresh dual rerun imported; all primary rows passed EVAS/Spectre certification.

## Notes

- Only primary gold/fixed pass bundles are imported into the release denominator.
- Bugfix buggy companion bundles remain separate badcase evidence and are not scored here.
- Partial stale-count import is conservative: it imports only exact current release entry/form matches.

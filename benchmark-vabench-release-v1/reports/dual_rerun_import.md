# vaBench Release Dual Rerun Import

Date: 2026-06-22

This report records whether fresh release EVAS/Spectre rerun results
were imported into release evidence. It does not import blocked, dry-run,
or still-running summaries.

## Summary

| Metric | Value |
| --- | ---: |
| status | `imported` |
| stale summary | `False` |
| summary tasks total | 8 |
| current queue count | 0 |
| imported primary results | 0 |
| skipped results | 0 |
| imported pass | 0 |
| imported pending | 0 |
| imported fail | 0 |

Reason: No current dual rerun queue remains; dual_certification.json already reflects imported fresh rerun evidence.

## Notes

- The import step is idempotent once the current rerun queue is empty and dual certification is complete.
- Rerun timing and model-baseline claims remain separate gates.

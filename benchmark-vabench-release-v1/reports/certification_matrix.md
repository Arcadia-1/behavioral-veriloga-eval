# vaBench Release Certification Matrix

Date: 2026-05-26

This matrix is a paper-facing audit view over the release certification
state. It reorganizes existing evidence and does not create new
simulator certification evidence.

## Summary

| Metric | Value |
| --- | ---: |
| status | `partial` |
| entries | 64 |
| forms | 219 |
| fully certified entries | 63 |
| pending entries | 1 |
| certified forms | 217 |
| pending forms | 2 |
| fresh dual-rerun pending forms | 2 |
| source-equivalence blocked forms | 0 |
| dual-failure forms | 0 |
| EVAS PASS / Spectre FAIL | 0 |
| scored entries | 51 |
| scored forms | 184 |

## Entry Pending Cause Counts

- `fresh_dual_rerun_pending`: 1
- `fully_certified`: 63

## Form Pending Cause Counts

- `certified`: 217
- `fresh_dual_rerun_pending`: 2

## Form Disposition Counts

- `fresh_dual_rerun_required`: 2
- `none`: 217

## Source-Equivalence Blocked Forms

- none

## Claim Boundary

- This matrix reorganizes existing release certification evidence; it does not create new simulator evidence.
- Only forms with static/evas/spectre pass and counted_in_score=true may enter benchmark scores.
- Pending fresh dual rerun and source-equivalence blocked forms remain excluded from score and full-release claims.

# vaBench Release Package Manifest

Date: 2026-05-29

This package-level manifest indexes every release entry and materialized
form. It is a navigation and machine-consumption layer, not simulator
certification evidence.

## Summary

| Metric | Value |
| --- | ---: |
| status | `in_progress` |
| planned entries | 79 |
| entries | 79 |
| forms | 271 |
| core entries | 66 |
| support entries | 13 |
| core forms | 236 |
| support forms | 35 |
| content denominator entries | 66 |
| content-excluded entries | 13 |
| content denominator forms | 236 |
| content-excluded forms | 35 |
| certified entries | 79 |
| certified forms | 271 |
| pending entries | 0 |
| pending forms | 0 |
| scored entries | 66 |
| scored forms | 236 |
| core scored entries | 66 |
| core scored forms | 236 |
| support scored entries | 0 |
| support scored forms | 0 |
| L0 conformance cases | 4 |

## Entry Status Counts

| Status | Count |
| --- | ---: |
| `certified` | 79 |

## Form Status Counts

| Status | Count |
| --- | ---: |
| `certified` | 271 |

## Claim Boundary

- This manifest is an index over package assets and reports; it is not simulator certification evidence.
- Rows with counted_in_score=false must not enter benchmark score denominators.
- Rows with content_denominator_included=false remain package assets but are excluded from strong benchmark content claims.
- Rows with track=support are auxiliary measurement/stimulus assets and must be reported separately from the core circuit score.
- Imported subset certification must not be phrased as full release certification.
- claim_gate_status=in_progress

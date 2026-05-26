# vaBench Release Package Manifest

Date: 2026-05-26

This package-level manifest indexes every release entry and materialized
form. It is a navigation and machine-consumption layer, not simulator
certification evidence.

## Summary

| Metric | Value |
| --- | ---: |
| status | `in_progress` |
| planned entries | 64 |
| entries | 64 |
| forms | 219 |
| core entries | 51 |
| support entries | 13 |
| core forms | 184 |
| support forms | 35 |
| content denominator entries | 51 |
| content-excluded entries | 13 |
| content denominator forms | 184 |
| content-excluded forms | 35 |
| certified entries | 63 |
| certified forms | 217 |
| pending entries | 1 |
| pending forms | 2 |
| scored entries | 51 |
| scored forms | 184 |
| core scored entries | 51 |
| core scored forms | 184 |
| support scored entries | 0 |
| support scored forms | 0 |
| L0 conformance cases | 4 |

## Entry Status Counts

| Status | Count |
| --- | ---: |
| `certified` | 63 |
| `pending` | 1 |

## Form Status Counts

| Status | Count |
| --- | ---: |
| `certified` | 217 |
| `pending` | 2 |

## Claim Boundary

- This manifest is an index over package assets and reports; it is not simulator certification evidence.
- Rows with counted_in_score=false must not enter benchmark score denominators.
- Rows with content_denominator_included=false remain package assets but are excluded from strong benchmark content claims.
- Rows with track=support are auxiliary measurement/stimulus assets and must be reported separately from the core circuit score.
- Imported subset certification must not be phrased as full release certification.
- claim_gate_status=in_progress

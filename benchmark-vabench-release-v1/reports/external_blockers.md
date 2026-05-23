# vaBench Release External Blockers

Date: 2026-05-24

This report isolates the non-certification blockers that prevent the
release package from becoming fully paper-claimable. It is a recovery
and claim-boundary artifact, not simulator certification evidence.

## Summary

| Metric | Value |
| --- | ---: |
| status | `pending` |
| blockers | 1 |
| blocked | 0 |
| pending | 1 |
| ready-to-continue | 0 |
| bridge status | `ready` |
| primary rerun queue rows | 0 |
| ready staging bundles | 0 |
| latest rerun summary | `complete` |
| latest import | `partial_imported` |

## Blockers

| ID | Status | Scope | Diagnosis |
| --- | --- | --- | --- |
| `B4_downstream_paper_claims_disabled` | `pending` | speed/debug, model baseline artifacts | downstream paper claims remain disabled until their dedicated artifacts are explicitly enabled |

## Recovery Sequence

- Fix external SSH/VPN/jump-host reachability until bridge diagnostics reports a ready profile.
- Run finish_after_bridge without --dry-run to execute the fresh release dual rerun.
- Import only a complete current rerun summary, then regenerate paper artifacts and completion audit.
- Enable scored benchmark and baseline artifacts only after dual certification has no pending release forms.

## Claim Boundary

- This report is blocker/recovery evidence only; it is not EVAS/Spectre certification evidence.
- A blocked or dry-run simulator summary must not be imported into release evidence.
- Score, speed, and baseline claims remain governed by their dedicated claim gates.

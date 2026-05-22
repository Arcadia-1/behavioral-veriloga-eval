# vaBench Release Finish-After-Bridge Attempt

Date: 2026-05-19

This report records attempts to finish the release after the external
Virtuoso bridge becomes available. It does not turn blocked runs into
certification evidence.

## Summary

| Metric | Value |
| --- | --- |
| status | `dry_run` |
| reason | dry run: no bridge tunnel or simulator command was executed |
| profiles | `default, ci, jin` |
| bridge diagnostics | `ready` |
| ready profiles | `default, ci, jin` |
| completion audit | `in_progress` |

## Rerun Scope

| Metric | Value |
| --- | --- |
| queue status | `complete` |
| primary queue rows | 0 |
| ready primary rows | 0 |
| staging bundles | 0 |
| ready staging bundles | 0 |
| include buggy variants | `False` |
| latest summary status | `dry_run` |
| latest import status | `imported` |
| latest import stale summary | `False` |

## Attempts

| Profile | Status | Return code | Reason |
| --- | --- | ---: | --- |
| `default` | `planned` |  |  |
| `ci` | `planned` |  |  |
| `jin` | `planned` |  |  |

## Next Actions

- Fix SSH/tunnel reachability for at least one bridge profile if all attempts are blocked.
- Re-run this script without --dry-run after bridge diagnostics reports a ready profile.
- Import only complete rerun summaries; blocked summaries remain non-certification evidence.

# vaBench Release Finish Readiness

Date: 2026-05-26

This report states whether it is safe to start or import the fresh
EVAS/Spectre release rerun. It is a readiness gate, not simulator
certification evidence.

## Summary

| Metric | Value |
| --- | --- |
| status | `ready_to_run` |
| ready to run fresh dual | `True` |
| ready to import fresh dual | `False` |
| ready to finish release | `False` |
| passed checks | 4 |
| blocked checks | 3 |

## Checks

| ID | Status | Finding |
| --- | --- | --- |
| `P1_local_release_package_ready` | `pass` | planned=64, source_linked=64, materialized=64, asset=pass, static=pass |
| `P2_primary_rerun_queue_ready` | `pass` | queue_status=ready, queue_count=2, ready=2, blocked=0 |
| `P3_staging_ready` | `pass` | queue_rows=2, ready_primary_rows=2, bundles=2, ready_bundles=2, blocked_bundles=0 |
| `P4_bridge_ready` | `pass` | bridge_status=ready, ready_profiles=['default', 'ci', 'jin'], reason=bridge profile default is ready for release rerun |
| `P5_current_summary_acceptable` | `blocked` | summary_status=complete, tasks_total=2, queue_count=2, dry_run=False, expected_miss_count=2 |
| `P6_import_gate_clear` | `blocked` | import_status=imported, stale_summary=False, imported=2 |
| `P7_full_dual_certification_clear` | `blocked` | dual_pending=2, dual_failed=0, evas_pass_spectre_fail=0 |

## Fresh Summary Acceptance Criteria

- summary.status == complete
- summary.tasks_total matches the active queue before import, or matches the imported full-rerun summary after certification import
- summary.dry_run is false or absent
- summary.expected_miss_count == 0
- dual_rerun_import.json is not stale after import

## Commands

| Command | Value |
| --- | --- |
| `refresh_local_package` | `python3 runners/run_vabench_release_longrun.py` |
| `refresh_bridge_diagnostics` | `python3 runners/report_vabench_release_bridge_diagnostics.py --ssh-timeout-s 10` |
| `dry_run_finish_plan` | `python3 runners/finish_vabench_release_after_bridge.py --dry-run --no-refresh-reports` |
| `finish_after_bridge` | `python3 runners/finish_vabench_release_after_bridge.py` |
| `direct_primary_rerun` | `./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py --output-root results/vabench-release-v1-dual-rerun --timeout-s 180` |

## Claim Boundary

- This readiness report is not simulator certification evidence.
- A ready queue or ready staging bundle does not imply EVAS/Spectre pass.
- A stale, blocked, dry-run, or partial summary must not be imported.

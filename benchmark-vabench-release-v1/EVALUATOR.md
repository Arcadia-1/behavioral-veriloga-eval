# vaBench Release Evaluator Contract

Date: 2026-05-26

This contract describes how the release package is consumed by evaluators
and paper-facing baselines. It does not create certification evidence.

## Task Selection

| Metric | Value |
| --- | ---: |
| package entries | 64 |
| package forms | 219 |
| certified entries | 63 |
| certified forms | 217 |
| scored entries | 51 |
| scored forms | 184 |
| L0 conformance excluded | `True` |

## Backend Roles

| Backend | Role | Final judge |
| --- | --- | --- |
| `static` | source/package integrity gate | `False` |
| `evas` | fast behavioral Verilog-A filter and debug evaluator | `False` |
| `spectre` | final simulator reference for release certification and scoring | `True` |

## Gates

- Score gate: `score_enabled`; scored entries/forms = 51/184
- Finish readiness: `ready_to_run`
- Baseline gate: `pending_release_baselines`; claim allowed = `False`
- Speed/debug gate: `measured_with_failures`; claim allowed = `False`

## Commands

| Command | Value |
| --- | --- |
| `refresh_package` | `python3 runners/run_vabench_release_longrun.py` |
| `finish_after_bridge` | `python3 runners/finish_vabench_release_after_bridge.py` |
| `primary_dual_rerun` | `./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py --output-root results/vabench-release-v1-dual-rerun --timeout-s 180` |
| `enable_score_denominator` | `python3 runners/enable_vabench_release_score_denominator.py` |
| `refresh_score_denominator` | `python3 runners/report_vabench_release_score_denominator.py` |
| `refresh_baseline_gate` | `python3 runners/report_vabench_release_baseline_artifact.py` |

## Claim Boundary

- This contract defines evaluator IO and score gates; it is not simulator certification evidence.
- Spectre is the final judge for release scoring.
- EVAS is a fast filter/debug evaluator and cannot certify a task by itself.
- L0 conformance cases are evaluator health checks and never scored benchmark rows.
- Baseline and speed/debug claims remain blocked until their dedicated artifacts allow them.
- claim_gate_status=in_progress

# vaBench Release Evaluator Contract

Date: 2026-06-01

This contract describes how the release package is consumed by evaluators
and paper-facing baselines. It does not create certification evidence.

## Task Selection

| Metric | Value |
| --- | ---: |
| package entries | 79 |
| package forms | 271 |
| certified entries | 79 |
| certified forms | 271 |
| scored entries | 66 |
| scored forms | 236 |
| L0 conformance excluded | `True` |

## Backend Roles

| Backend | Role | Final judge |
| --- | --- | --- |
| `static` | source/package integrity gate | `False` |
| `evas` | fast behavioral Verilog-A filter and debug evaluator | `False` |
| `spectre` | final simulator reference for release certification and scoring | `True` |

## Gates

- Score gate: `score_enabled`; scored entries/forms = 66/236
- Finish readiness: `ready_to_run`
- Baseline gate: `claim_ready`; claim allowed = `True`
- Speed/debug gate: `pending_measurement`; claim allowed = `False`

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
- Baseline and speed/debug claims are independent dedicated gates; one may be allowed while the other remains blocked.
- Model baselines must use the fixed scored denominator and report hygiene slices when claimable.
- claim_gate_status=in_progress

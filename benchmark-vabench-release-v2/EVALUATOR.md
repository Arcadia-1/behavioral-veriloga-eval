# vaBench Release v2 Evaluator Contract

Date: 2026-06-24

Status: `under_construction`

## Prompt Protocol

- Agent-visible source: `agent_visible_files.json -> public/agent_visible_spec.md + agent_prompt.md + allowlisted public/support artifacts`
- Agent-visible spec filename: `public/agent_visible_spec.md`
- Agent prompt filename: `agent_prompt.md`
- Hidden sources:
  - `task_release_card.json`
  - `private/invisible_checker_config.yaml`
  - `private/invisible_spec_checker_map.json`
  - `private/gold/*`
- Spec-checker map audit: `benchmark-vabench-release-v2/scripts/audit_spec_checker_map.py`

## Evaluation Protocol

- primary_track: `one_shot`
- feedback_track: `deferred`
- score_mixing_policy: Do not mix one-shot scores and feedback/debug pass@K scores in the same denominator.

## Claim Gate

- score_claim_allowed: `False`
- blocking_reason: Fresh v2 EVAS/Spectre certification has not been rerun for migrated rows.

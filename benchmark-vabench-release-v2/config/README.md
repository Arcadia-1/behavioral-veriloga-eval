# vaBench v2 Config

This directory is the release-local control surface for v2. New tasks should not
require runner code changes or global repository settings changes.

## Files

- `release_config.json` defines release identity, task discovery, generated
  package outputs, prompt visibility rules, evaluation protocol, score policy,
  and evaluator backend roles.

## Current Protocol Decision

The active v2 benchmark track is `one_shot`. Feedback-style debug evaluation is
reserved for a later separate track and must not share the same score
denominator.

Each task form now separates the public contract into:

- `public/agent_visible_spec.md`: canonical agent-visible functional
  specification and the public source checker intent must trace to.
- `agent_prompt.md`: thin agent wrapper rendered with
  `public/agent_visible_spec.md` by the v2 prompt renderer.
- `agent_visible_files.json`: allowlist of files rendered to the evaluated
  agent and target files expected back.
- `private/invisible_checker_config.yaml`: checker/evaluator config hidden from
  the agent.
- `private/invisible_spec_checker_map.json`: private map from public spec
  requirements to checker config and executable checker functions.

Release config records this protocol through
`prompt_protocol.agent_visible_spec_filename` and
`prompt_protocol.agent_visible_source`. Legacy v2 task names are still accepted
during migration.

For human inspection of task-form directories, use the layer map in
`../TASK_FORM_LAYOUT.md`.

## Replacement Rule

Future runners should accept a single `--release-root` or `--config` argument.
When pointed at `benchmark-vabench-release-v2/config/release_config.json`, they
should discover all v2 paths from this file instead of hard-coding v1 paths.

Per-task migration remains local to each task form. The release-level config
does not need to change for each migrated benchmark unless the v2 protocol
itself changes.

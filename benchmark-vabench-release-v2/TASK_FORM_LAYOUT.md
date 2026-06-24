# vaBench v2 Task Form Layout

This document is for human readers. It explains how to read one task-form
directory without confusing agent-visible inputs, private evaluator assets, and
release metadata.

## Directory Shape

```text
forms/<form>/
  agent_prompt.md
  agent_visible_files.json
  task_release_card.json
  public/
    agent_visible_spec.md
    support/
  private/
    invisible_checker_config.yaml
    invisible_spec_checker_map.json
    gold/
```

## Layers

| Layer | Files | Solver Visible | Purpose |
| --- | --- | --- | --- |
| Agent-visible task contract | `agent_prompt.md`, `public/agent_visible_spec.md` | Yes | Defines the task statement and functional specification shown to the evaluated agent. |
| Public support inputs | `public/support/*` | Only if allowlisted | Provides read-only testbenches or buggy sources. |
| Agent-visible file manifest | `agent_visible_files.json` | No | Declares the exact files the renderer may show to an agent. It should not contain private checker thresholds or answer hints. |
| Private task card | `task_release_card.json` | No | Records release metadata, provenance, diagnostics, artifacts, certification state, and score status. |
| Invisible checker config | `private/invisible_checker_config.yaml` | No | Declares the executable checker task id plus syntax, observable, backend, thresholds, and private checking policy. |
| Invisible spec-checker map | `private/invisible_spec_checker_map.json` | No | Links public requirements to checker config IDs and executable checker functions, and stores private forbidden-leak terms for prompt-boundary audits. |
| Private reference assets | `private/gold/*` | No | Stores gold solutions or reference artifacts for validation. |

## Public/Private Rule

The only agent-visible task material is the rendered prompt produced from
`agent_visible_files.json`:

```text
agent_prompt.md
+ public/agent_visible_spec.md
+ allowlisted public/support/*
```

Everything under `private/` plus `task_release_card.json` is evaluator-only.
The prompt-boundary and spec-checker map audits enforce that private checker
IDs, private thresholds, sample windows, root causes, and gold implementations
do not appear in the rendered agent prompt.

Current v2 task directories should use only the agent/invisible names above.
Readers may retain legacy compatibility for historical drafts, but release
candidate task directories should not use legacy draft filenames.

## Why `agent_prompt.md` Points To `public/agent_visible_spec.md`

`agent_prompt.md` is intentionally short. It states the task and output
contract. `public/agent_visible_spec.md` is the canonical agent-visible
functional specification that both humans and checkers should trace back to.

This split prevents public prompts from becoming mixed with private benchmark
headers, checker implementation details, or repair diagnostics. It also lets
human reviewers inspect one stable public contract per task.

## Checker Boundary

`private/invisible_checker_config.yaml` is consumed by the evaluator. It
declares the executable checker task id and keeps task-local syntax,
observables, backend, thresholds, and private checking policy next to the
benchmark assets. The executable waveform decision procedure still lives in
runner code.

The intended relationship is:

```text
public/agent_visible_spec.md
  -> private/invisible_spec_checker_map.json links public anchors to private checks
  -> private/invisible_checker_config.yaml declares evaluator config and private check IDs
  -> Python checker implements the waveform decision procedure
```

If these four drift, the task should be audited before it is score-enabled.

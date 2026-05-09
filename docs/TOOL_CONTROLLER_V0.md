# vaEVAS Tool Controller v0.3

Date: 2026-05-08

## Goal

The tool controller turns strict-EVAS feedback into explicit tool-routing
decisions.  It is not a stronger code generator by itself.  Its current purpose
is cost-aware scheduling:

1. Extract a structured repair state from validator feedback.
2. Try cheap deterministic compile tools.
3. Route selected families to expensive CE/LLM fallback tools.
4. Treat local and fallback outputs as competing candidates, then select the
   best strict-EVAS rank.
5. Record traces that can later train a learned controller.

## State

`RepairState` is written into each final `generation_meta.json`, the controller
manifest, and the trace files.  It includes:

| Field | Meaning |
| --- | --- |
| `task_id` | Benchmark task id. |
| `status` | Current strict-EVAS status. |
| `task_form` | Public task form, such as `tb-generation` or `spec-to-va`. |
| `core_function` | Benchmark circuit/function family. |
| `required_axes` | Required scoring axes from task metadata. |
| `failure_families` | Routed diagnostic families, such as `empty_pwl` or `single_sourced_port`. |
| `scores` | Current `dut_compile`, `tb_compile`, `sim_correct`, `weighted_total`. |
| `notes` | Public validator notes used for routing. |

## Tools

The current controller exposes two tool classes:

| Tool | Type | Cost | Role |
| --- | --- | ---: | --- |
| `local_compile_skill_batch` | deterministic local | 0 LLM calls | Applies safe compile-skill fixers and accepts only if strict-EVAS compile rank improves. |
| `cached_llm_ce_fallback` | cached LLM/CE fallback | projected from cached meta plus local re-score time | Reuses CE-v2 candidate code to evaluate routing without new API spend; the candidate must be re-scored with current strict-EVAS before acceptance. |

Future tools should keep the same action record shape:

```json
{
  "tool": "module_contract_repair",
  "tool_type": "deterministic_local",
  "decision": "accepted",
  "before_status": "FAIL_TB_COMPILE",
  "after_status": "PASS",
  "projected_usage": {}
}
```

## Policies

| Policy | Intention | Current routing rule |
| --- | --- | --- |
| `never` | Local-only ablation. | Never route CE/LLM fallback. |
| `pass-efficient` | Maximize PASS per token. | Route only high-confidence PASS families: compile-only empty PWL and single sourced-port with gold DUT include. |
| `compile-coverage` | Maximize compile closure for later behavior repair. | Route all empty-PWL cases plus single sourced-port with gold DUT include. |
| `all-compile` | CE/LLM fallback upper bound. | Route every selected compile failure. |

## Candidate Arbitration

The controller uses `--fallback-routing-state` to decide which repair-state
view can trigger CE/LLM fallback:

| Mode | Meaning |
| --- | --- |
| `initial` | Route only from the first strict-EVAS failure state. |
| `current` | Route only after deterministic local tools have run. |
| `either` | Route if either the initial or post-local state requests fallback. |

The default is `either`.  This avoids a sequential-control pitfall: a local
compile skill may improve a task from compile failure to behavior failure, but a
CE candidate routed from the initial signal may still be better.  The controller
therefore evaluates the fallback candidate independently and accepts it only if
its current strict-EVAS rank is higher than the current selected candidate.

Cached fallback results are not trusted as final scores.  The cached code is
re-scored with current strict-EVAS, and accepted cached actions must include
`cached_verified=true`.

## Reward

The default scalar reward is for analysis and future learned routing only:

```text
reward =
  10.0 * pass_gain
+  2.0 * compile_gain
+  2.0 * behavior_gain
-  0.02 * total_tokens / 1000
-  0.01 * api_elapsed_s
```

These weights are configurable through CLI flags.  The reward should not be used
as the sole paper metric; report PASS, compile closure, token, and time
separately.

## Trace Artifacts

Each controller run writes:

| Artifact | Purpose |
| --- | --- |
| `tool_controller_manifest.json` | Full manifest with per-task state, actions, projected usage, reward, and summary. |
| `tool_controller_trace.jsonl` | One JSON row per task, suitable for learned-controller datasets. |
| `tool_controller_trace.csv` | Flat table for quick inspection. |
| `sample_0/generation_meta.json` | Final candidate metadata with selected source and projected controller cost. |

Use `--selected-only` for small smoke runs so cost summarizers only see the
selected tasks.

## Current Smoke Result

Seven residual compile tasks were evaluated with cached CE-v2 fallback.

The original v0.2 smoke trusted cached result files and reported `2/7` PASS for
the routed controller rows.  A current strict-EVAS re-score found that one cached
PASS was stale.  v0.3 fixes this by re-scoring cached candidates before
acceptance.

| Row | Routed CE calls | strict-EVAS PASS | TB compile rate | Total tokens | API seconds | Local eval seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Controller `pass-efficient` v0.3 | 2 | 1/7 | 2/7 | 7426 | 12.294 | 1.255 |
| Controller `compile-coverage` v0.3 | 3 | 1/7 | 3/7 | 11739 | 19.552 | 1.636 |

Interpretation: controller routing is still valuable as a cost-aware scheduler,
but it does not improve the current PASS ceiling on this residual slice.  Its
confirmed benefit is compile-state triage and token/time reduction for selected
CE probes, not behavior repair.

## Audit Guardrails

Use `runners/audit_tool_controller_run.py` after every controller smoke.  The
audit checks:

1. Manifest, trace, sample metadata, and result-root task counts match.
2. Per-task and summary token/time totals agree.
3. Source-selected tasks do not inherit stale LLM cost.
4. Accepted cached fallback actions have usage metadata.
5. Accepted cached fallback actions were re-scored with current strict-EVAS.
6. Manifest final status matches the independently re-scored result root.

## Next Tools

The next quality gain should come from stronger execution tools:

1. Public-contract module-header port-order repair.
2. Required-module alias/wrapper materialization.
3. Multi-output sourced-port rebuild.
4. Behavior-repair tools after compile closure is stable.

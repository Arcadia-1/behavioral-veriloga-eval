# V4 Calibration Pilot

The default release target is `benchmark-vabench-release-v4/release/benchmarkv4`.
Use `--sample-families N --seed S` for reproducible random complete-family
campaigns, or pass an explicit `--selection` manifest when reproducing a
historical pilot. `CALIBRATION_FAMILIES.json` is retained only as historical
selection evidence.

The pilot is used only to freeze generic form skills, the generic feedback
skill, the agent wall-time cap, provider per-turn output cap, safety limits,
runner behavior, repetition count, and telemetry. Skill text must remain task-agnostic. Form-writing skills are
derived from installed Cadence/Spectre help; feedback skills describe the
project-authored vaBench facility. Neither may contain a selected family ID,
title, equation, threshold, stimulus constant, checker rule, or mutation hint.

Because model outcomes from these families influence experimental settings,
their 30 forms are excluded from the primary post-calibration result. The
primary denominator is therefore 390 families and 1,170 scored forms. The
complete 400-family result may be reported only as a clearly labeled secondary
or sensitivity analysis.

The selection does not modify task assets, existing EVAS/Spectre evidence, or
the sealed 1,200-task release. A later campaign manifest must reference this
file by SHA-256 and record the frozen parameters produced by the pilot.

## Build The Campaign

The calibrated primary episode limit is wall-clock time: by default each agent
episode gets 5,400 seconds, while setup, model requests, tool calls, and judges
use 1,800-second infrastructure ceilings. The provider token value is
`per_turn_max_tokens`: a per-model-call safety cap passed as `max_tokens`, not a
cumulative G0-G5 stopping budget. Provider completion, hidden reasoning, visible
completion, and feedback-delivered text are recorded as telemetry and must be
reported separately from functional score.

If a model/provider rejects the next turn because the conversation exceeds its
native context window, the runner records `context_window_exceeded` separately.
If a single call stops at the provider output cap, the runner records
`termination_reason=model_output_limit`; it does not treat accumulated tokens as
the experimental ability budget. If wall time expires, the latest valid
workspace artifact is still eligible for judging, and otherwise the cell is
reported as `agent_timeout`.

```bash
python3 benchmark-vabench-release-v4/operations/calibration_pilot/build_campaign.py \
  --sample-families 10 \
  --seed 20260715 \
  --model qwen3.5-flash \
  --per-turn-max-tokens 65536 \
  --repetitions 1 \
  --output /tmp/v4-api-pilot-campaign.json
```

This produces 180 cells: ten families, three forms, and six modes. Use
`--repetitions` only after the single-episode smoke is sound.

Each model event records the requested per-turn maximum, provider-reported
completion, reasoning and visible tokens, and `finish_reason`. Hosted-model
aliases and provider timestamps must also be retained in external run metadata.

## Reuse A Completed Pilot

Completed episodes may be mechanically reused only when the model, prompt hash,
release hash, selection hash, endpoint hash, decoding settings, wall-time
policy, per-turn token cap, tools, and candidate files are unchanged. Prepare a
derived runtime containing only mechanically eligible episodes:

```bash
python3 benchmark-vabench-release-v4/operations/calibration_pilot/prepare_budget_reuse.py \
  --source-output /tmp/v4-calibration-4096 \
  --source-campaign /tmp/v4-calibration-4096.json \
  --target-campaign /tmp/v4-calibration-65536.json \
  --output /tmp/v4-calibration-65536
```

`REUSE_MANIFEST.json` records every accepted or rejected cell, source-result
hashes, candidate hashes, and rejection reasons. Reuse requires the same
provider, model, endpoint hash, temperature, streaming mode, prompt, feedback
adapter hash, wall-time policy, per-turn token cap, and release. A submitted
file is not by itself reusable: any episode whose model turn hit the provider
output limit must be rerun because an agent may have written an intermediate
file before truncation.
Run the full target campaign with `--resume`; reused cells are skipped and all
rejected cells start fresh.

## Dry Run

Dry-run exports isolated runtime packages without contacting a model:

```bash
python3 benchmark-vabench-release-v4/operations/calibration_pilot/run_campaign.py \
  --campaign /tmp/v4-calibration-campaign.json \
  --output /tmp/v4-calibration-dryrun \
  --dry-run --limit 18
```

Each runtime exposes only `public/task` and `public/submission` to an agentic
model. Evaluator assets remain outside the model mount. G0 parses exact
artifact blocks into the submission directory without tools. G1 still makes
one final artifact-envelope submission, but may inspect an optional read-only
skill tree through `list_skills` and `read_skill` when `--skill-root` is set.
It cannot write files, call feedback, or finalize through tools. G2-G5 expose
bounded file tools, the injected feedback adapter, and `finalize`; G3/G5 may
also inspect the same read-only skill tree when configured.

Direct responses must use the exact artifact envelope contract. The live runner
rejects filename-only markers, input-artifact markers, Markdown fences,
duplicate or out-of-order blocks, undeclared paths, and non-whitespace text
outside the blocks. It preserves the extracted body bytes and records the raw
response hash, parser version, diagnostics, and artifact hashes. A format
failure remains `invalid_submission` and is not passed to a judge.

`audit_direct_protocol.py` can classify deterministic recoverability in stored
historical responses. `reparse_direct.py` may materialize those recovered files
under `evidence/recovered_direct_submission` for diagnosis, but it does not
change the episode status or make the result score-eligible. Recovery therefore
stays separate from the benchmark execution path.

## Provider Credentials

Credentials are loaded from an environment variable or a repository-external
file and are never included in prompts or result JSON. Credential-file paths
and injected operator commands are redacted from wrapper metadata:

```bash
export DEEPSEEK_API_KEY='...'
python3 benchmark-vabench-release-v4/runners/run_benchmarkv4_campaign.py \
  --task-id v4-001 \
  --mode G0 \
  --model deepseek-v4-flash \
  --base-url https://api.deepseek.com/v1 \
  --api-key-env DEEPSEEK_API_KEY \
  --output-root /tmp/benchmarkv4-api-smoke
```

The provider adapter uses the OpenAI-compatible chat-completions protocol.
Changing providers requires only `--base-url`, the campaign model ID, and
`--api-key-env` or `--api-key-file`.

`run_benchmarkv4_campaign.py` uses the release-pinned
`skill_lookup/veriloga-skills` snapshot by default for skill-enabled modes
(G1/G3/G5). Pass `--no-skill-root` only for an explicit no-skill ablation, or
`--skill-root <path>` to test another pinned candidate. The model sees only
relative read-only skill paths and file contents requested through the skill
tools. The wrapper records a tree hash for reproducibility and redacts the
local path from metadata.

## Evaluator Adapters

`--feedback-command` and `--final-judge-command` inject benchmark-controlled
commands. They receive these environment variables:

- `VABENCH_RUNTIME_DIR`
- `VABENCH_PUBLIC_DIR`
- `VABENCH_SUBMISSION_DIR`
- `VABENCH_EVALUATOR_DIR`

The feedback adapter may run EVAS and return public diagnostics. The final
judge adapter runs once after submission and may dispatch Spectre remotely.
Neither command string nor evaluator directory is sent to the model. A formal
pilot must configure both adapters; a provider-only smoke may omit them only to
test API transport and direct artifact parsing.

By default, the runner returns a compact feedback payload to the model: oracle
summary lines, validation diagnostics, and concrete errors are retained, while
verbose simulator counters are omitted from the conversation to preserve the
provider context window. Use `--feedback-output-mode raw` only when intentionally
reproducing older runner behavior or debugging the feedback adapter itself.

The repository-native EVAS adapter is:

```bash
--feedback-command \
  "python3 benchmark-vabench-release-v4/operations/calibration_pilot/feedback_adapter.py"
```

For DUT and Bugfix it invokes the family-specific behavior oracle. For
Testbench it runs the submitted deck on the supplied correct DUT and the
publicly queryable anonymous mutation subset. It returns diagnostics only; it
does not expose source mutations, checker code, or final score cases.

Generated campaign manifests, runtime workspaces, API responses, simulator
outputs, and credentials belong outside the repository. Only runner source,
tests, schemas, and compact aggregate reports should enter a PR.

## Score A Completed Campaign

Run a judge adapter over every complete submission and aggregate model, form,
mode, token, tool, and outcome records:

```bash
python3 benchmark-vabench-release-v4/operations/calibration_pilot/score_campaign.py \
  --campaign-output /tmp/v4-calibration-smoke \
  --judge-kind feedback_evas \
  --judge-command \
    "python3 benchmark-vabench-release-v4/operations/calibration_pilot/feedback_adapter.py"
```

`score_campaign.py` resolves campaign/output paths and existing judge-command
script paths to absolutes before invoking adapters, so the command is safe to
run from either the workspace root or `behavioral-veriloga-eval/`.

`feedback_evas` reports are always marked `provisional_feedback_only`; they
are useful for pilot tuning but are not benchmark scores. A paper-facing run
must use `--judge-kind final_spectre` with the sealed Spectre adapter. Missing
or invalid submissions remain explicit denominator failures and are never
silently dropped.

Historical pilot runs produced before submission-path normalization can be
repaired without another model call when every required candidate is found
under one unique common extra directory and no competing target copy exists:

```bash
python3 benchmark-vabench-release-v4/operations/calibration_pilot/repair_submission_layout.py \
  --campaign-output /tmp/v4-calibration-smoke
```

The repair is path-only, preserves artifact hashes, and records the stripped
prefix and each promotion. It rejects partial bundles, symlinks, and ambiguous
or competing prefixes. Recovered candidates remain
`submission_protocol_compliant=false`, and the formal scorer treats them as not
submitted.

Long agentic episodes checkpoint the public conversation, cumulative provider
output tokens, tool events, and current submission after every model and tool action.
`--resume` continues the same episode after an infrastructure interruption;
it does not reset the wall-time episode budget, create another sample, or grant another
pass@k opportunity.

Independent cells may run concurrently with `--workers N`. Each worker writes
only its own cell runtime; keep `--workers 1` when diagnosing provider rate
limits or simulator resource contention.

# V4 Calibration Pilot

The default release target is `benchmark-vabench-release-v4/release/benchmarkv4`.
Use `--sample-families N --seed S` for reproducible random complete-family
campaigns, or pass an explicit `--selection` manifest when reproducing a
historical pilot. `CALIBRATION_FAMILIES.json` is retained only as historical
selection evidence.

The pilot is used only to freeze generic form skills, the generic feedback
skill, the episode output-token cap, safety limits, runner behavior, repetition count,
and telemetry. Skill text must remain task-agnostic. Form-writing skills are
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

The calibrated cap is 65,536 provider output tokens per episode. Provider
`completion_tokens` includes hidden reasoning and visible completion. G0-G5
share the same cumulative cap; tool output is recorded separately and does not
consume the model-generation budget. Episodes stop early on normal completion,
so 65,536 is a ceiling rather than a target consumption.

Local DeepSeek smoke tests showed that the 65,536-token ceiling can still be a
binding infrastructure limit for long agentic modes. In a five-testbench,
G0-G5 transport/evaluator smoke, all 30 cells submitted and no runner errors
occurred, but five cells reached the output budget; the strongest provisional
EVAS feedback was in G2-G4, while G5 showed diminishing returns. Treat
`submitted_at_budget` as a separate runner/setting signal when comparing modes,
and report hidden reasoning tokens separately from visible candidate text.
Future prompt or feedback changes should prefer compact diagnostics,
budget-aware stopping, and mode-specific round limits before increasing the
global cap.

```bash
python3 benchmark-vabench-release-v4/operations/calibration_pilot/build_campaign.py \
  --sample-families 10 \
  --seed 20260715 \
  --model qwen3.5-flash \
  --max-output-tokens 65536 \
  --repetitions 1 \
  --output /tmp/v4-api-pilot-campaign.json
```

This produces 180 cells: ten families, three forms, and six modes. Use
`--repetitions` only after the single-episode smoke is sound.

Each model event records the requested maximum, provider-reported completion,
reasoning and visible tokens, and `finish_reason`. Hosted-model aliases and
provider timestamps must also be retained in external run metadata.

## Reuse An Uncensored Pilot

Increasing a stopping cap does not invalidate an episode that completed
naturally before the old cap, provided the model, prompt hash, release hash,
selection hash, tools, and candidate files are unchanged. Prepare a derived
runtime containing only mechanically eligible episodes:

```bash
python3 benchmark-vabench-release-v4/operations/calibration_pilot/prepare_budget_reuse.py \
  --source-output /tmp/v4-calibration-4096 \
  --source-campaign /tmp/v4-calibration-4096.json \
  --target-campaign /tmp/v4-calibration-65536.json \
  --output /tmp/v4-calibration-65536
```

`REUSE_MANIFEST.json` records every accepted or rejected cell, source-result
hashes, candidate hashes, and rejection reasons. A submitted file is not by
itself reusable: any episode whose model turn hit the old output limit must be
rerun because an agent may have written an intermediate file before truncation.
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
model. Evaluator assets remain outside the model mount. G0/G1 parse exact
artifact blocks into the submission directory. G2-G5 expose bounded file
tools, the injected feedback adapter, and `finalize`.

Direct responses use exact artifact envelopes as the primary protocol. For a
task with exactly one target artifact, the runner also accepts recoverable
single-file containers: exactly one fenced code block, a filename-only marker
such as `<<<model.va>>>`, or an input-artifact marker whose path is the single
declared candidate path. These recoveries are recorded as non-strict
normalization protocols, not as exact-envelope compliance. For multi-file
tasks, a deterministic normalizer accepts only explicit, unique filename
labels attached to fenced blocks or sections. When labeled drafts precede
another bundle, it selects only the last complete bundle containing every
required filename once; it never mixes versions, maps by unlabeled block order,
repairs code, or inspects Verilog-A semantics. Exact-envelope compliance is
reported separately from functional score so transport formatting does not
masquerade as Verilog-A capability.

## Provider Credentials

Credentials are loaded from an environment variable or a repository-external
file and are never included in prompts, result JSON, or command arguments:

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
working-token budget. Use `--feedback-output-mode raw` only when intentionally
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
`submission_protocol_compliant=false`.

Long agentic episodes checkpoint the public conversation, cumulative provider
output tokens, tool events, and current submission after every model and tool action.
`--resume` continues the same episode after an infrastructure interruption;
it does not reset the token budget, create another sample, or grant another
pass@k opportunity.

Independent cells may run concurrently with `--workers N`. Each worker writes
only its own cell runtime; keep `--workers 1` when diagnosing provider rate
limits or simulator resource contention.

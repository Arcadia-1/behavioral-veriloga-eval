# V4 Calibration Pilot

The default release target is `benchmark-vabench-release-v4/release/benchmarkv4`.
Use `--sample-families N --seed S` for reproducible random complete-family
campaigns, or pass an explicit `--selection` manifest when reproducing a
historical pilot. `CALIBRATION_FAMILIES.json` is retained only as historical
selection evidence.

The pilot is used only to freeze generic form skills, the public EVAS guide,
the episode output-token cap, safety limits, runner behavior, repetition count,
and telemetry. Skill text must remain task-agnostic. Form-writing skills are
derived from installed Cadence/Spectre help; EVAS guides describe only the
public command-line contract. Neither may contain a selected family ID,
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
hashes, candidate hashes, and rejection reasons. Reuse requires the same
provider, model, endpoint hash, temperature, streaming mode, prompt, EVAS
executable identity, and release; only the output-token ceiling may increase. A
submitted file is not by itself reusable: any episode whose model turn hit the
old output limit must be rerun because an agent may have written an intermediate
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
model. Evaluator assets remain outside the model mount. G0/G1 parse exact
artifact blocks into the submission directory. G2-G5 expose bounded file
tools, restricted `run_evas`, and `finalize`. `run_evas` accepts no command
string: DUT/bugfix tasks run the fixed visible deck, while testbench tasks may
select only the reference or five public mutation fixtures declared by the
task-local `evas_runtime.json`.

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

## Evaluator Adapters

`--final-judge-command` injects the benchmark-controlled trusted replay. It
receives these environment variables:

- `VABENCH_RUNTIME_DIR`
- `VABENCH_PUBLIC_DIR`
- `VABENCH_SUBMISSION_DIR`
- `VABENCH_EVALUATOR_DIR`

The final judge adapter runs once after submission and may dispatch Spectre
remotely. Neither its command string nor evaluator directory is sent to the
model. A formal pilot must configure the final adapter; a provider-only smoke
may omit it only to test API transport and artifact handling.

### R45 result protocol

Every completed G0-G5 cell now writes an `experiment_result` object in
`evidence/campaign_result.json` conforming to
`schemas/vabench-experiment-result.schema.json`. The record preserves the exact
last assistant message and its hash, snapshots every declared final artifact
under `evidence/final_submission/`, and records per-file and tree hashes. This
snapshot is the scored submission; later edits to `public/submission` do not
change it. Trusted replay receives the snapshot path in both
`VABENCH_SUBMISSION_DIR` and `VABENCH_FINAL_SUBMISSION_DIR`, and its record binds
the replay to the snapshot tree hash.

The final judge is a trusted replay, not another model-feedback turn. Before it
runs, the runner hashes the exported evaluator tree and records
`evas --version` (override the executable with `--evas-command`). The adapter
must write JSON to `VABENCH_TRUSTED_REPLAY_RESULT` with one of these statuses:

```json
{
  "status": "behavior_failure",
  "diagnostics": ["first mismatch at 2.5e-9 s"]
}
```

Allowed terminal replay statuses are `passed`, `compile_failure`,
`runtime_failure`, `behavior_failure`, and `infrastructure_failure`. A legacy
adapter returning zero without JSON is accepted as `passed` with a compatibility
diagnostic. A nonzero return without JSON is an infrastructure failure because
the runner cannot safely infer its failure stage.

Model execution is separate from replay execution. `agent_timeout` and
`no_submission` have `score_eligible: false` and `score: null`; neither is
reported as a hidden-test or behavior zero. Trusted replay timeouts are
`runtime_failure`, while launch and malformed-result failures remain
`infrastructure_failure`.

The historical `feedback_adapter.py` remains only to reproduce old experiments.
It reads evaluator assets and must never be configured as an active G2-G5 model
tool. New runs use `run_evas`, which returns only raw public simulation output
from the fixed task-local contract and never invokes a checker or score oracle.

Generated campaign manifests, runtime workspaces, API responses, simulator
outputs, and credentials belong outside the repository. Only runner source,
tests, schemas, and compact aggregate reports should enter a PR.

## Score A Completed Campaign

Run a judge adapter over every complete submission and aggregate model, form,
mode, token, tool, and outcome records:

```bash
python3 benchmark-vabench-release-v4/operations/calibration_pilot/score_campaign.py \
  --campaign-output /tmp/v4-calibration-smoke \
  --judge-kind final_trusted_replay \
  --judge-command \
    "python3 /path/to/trusted_replay_adapter.py"
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
it does not reset the token budget, create another sample, or grant another
pass@k opportunity.

Independent cells may run concurrently with `--workers N`. Each worker writes
only its own cell runtime; keep `--workers 1` when diagnosing provider rate
limits or simulator resource contention.

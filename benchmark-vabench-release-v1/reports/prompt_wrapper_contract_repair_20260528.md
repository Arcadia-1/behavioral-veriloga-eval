# vaBench Prompt Wrapper Contract Repair

Date: 2026-05-28

## Purpose

This change separates benchmark prompt content from runner-side generation
protocol.  The public release prompts remain `public-contract-v3`; the model
baseline runner now records `release-runner-wrapper-v5` when sending prompts to
a model. The initial wrapper introduced the shared model I/O protocol; v4 adds
the include, unbounded-loop, and multiline-PWL safeguards found during the
DeepSeek failure attribution audit; v5 clarifies the Verilog-A include literals
after a manual review found that v4's Markdown-style backticks were ambiguous.

The boundary follows the VerilogEval v2 and CVDP prompt-construction lesson:
fixed interfaces, artifact names, output protocol, and simulator-language rules
are fair public contracts; hidden checker thresholds, gold control flow, and
reference implementations must remain private.

## What Changed

- Added `runners/vabench_release_prompt_wrapper.py`.
- Added runner-side `Question:` / `Answer:` structure.
- Added exact per-file output markers:
  - `[BEGIN file: <target>]`
  - `[DONE file: <target>]`
- Added shared EVAS/Spectre compatibility rules for:
  - voltage-domain-only Verilog-A,
  - no digital Verilog constructs in `.va`,
  - no current-domain/unsupported analog operators,
  - top-level event controls,
  - unconditional `transition(...)` contributions,
  - module-scope declarations,
  - fixed/genvar vector indexing,
  - Spectre `vsource` and AHDL instance syntax,
  - strictly increasing PWL times,
  - TB-as-stimulus/save-harness rather than checker generation.
- Updated `run_vabench_release_minimax_baseline.py` to send wrapped prompts,
  save both `public_prompt.md` and `prompt_sent.md`, and record
  `runner_wrapper_version` in generation metadata and summaries.
- Updated `prompt_contract_manifest` to record the runner wrapper version
  without changing the public prompt version.

### v1 -> v5 Follow-Up

The wrapper was tightened after the DeepSeek v4-pro full run exposed failures
that were not good model-capability evidence:

- Every generated `.va` file must explicitly include both `constants.vams` and
  `disciplines.vams`.
- Verilog-A candidates must avoid unbounded event loops such as `while (1)` and
  `forever`.
- Spectre PWL sources must use a single-line `wave=[ t0 v0 ... ]` form, or
  explicit backslash continuation when a line break is unavoidable.

Only rows whose old candidate failure is attributable to these wrapper-level
contract gaps should be regenerated for the v4 repair measurement. Runner
extraction failures and evaluator-review rows stay outside this prompt-rerun
slice.

The v4 include rule was later tightened to v5 because two rerun candidates
rendered the Verilog-A include directives without the leading Verilog-A
backtick. The v5 rule now describes the required include lines as explicit
literal text.

## Non-Changes

- No gold implementation code was copied into public prompts.
- No hidden checker thresholds or private sampling windows were added.
- No ICL/few-shot examples were added to benchmark public prompts.
- No public prompt version bump was made, because this is a runner-wrapper
  change rather than a benchmark-definition rewrite.

## Validation

- `python3 runners/report_vabench_release_prompt_contract_manifest.py`
  - result: `status=pass`, `prompt_version=public-contract-v3`, prompts `271`.
- `python3 runners/run_vabench_release_minimax_baseline.py --dry-run --limit 1 --tag wrapper-smoke --model dry-run-model`
  - result: dry-run completed and emitted wrapped `prompt_sent.md`.
- `PYTHONPATH=runners python3 -m pytest tests/test_vabench_release_prompt_wrapper.py tests/test_vabench_release_prompt_contract_manifest.py tests/test_vabench_release_prompt_contracts.py -q`
  - result: `9 passed`.
- `PYTHONPYCACHEPREFIX=/private/tmp/vaevas_pycache python3 -m py_compile runners/vabench_release_prompt_wrapper.py runners/run_vabench_release_minimax_baseline.py runners/report_vabench_release_prompt_contract_manifest.py`
  - result: pass.
- `git diff --check -- runners/report_vabench_release_prompt_contract_manifest.py tests/test_vabench_release_prompt_contract_manifest.py benchmark-vabench-release-v1/reports/prompt_contract_manifest.md benchmark-vabench-release-v1/reports/prompt_contract_manifest.json`
  - result: pass.
- `python3 runners/sync_vabench_release_prompt_contracts.py --dry-run`
  - result: 57 public prompt files would be mechanically normalized.
  - action: not applied in this repair because `prompt_contract_manifest` already
    passes and broad public prompt churn could overwrite task-level manual
    review. Public prompt edits should remain targeted to concrete
    checker-vs-contract gaps.

## Claim Boundary

Future model baseline reports must state both:

- public prompt version: `public-contract-v3`;
- runner wrapper version: `release-runner-wrapper-v5`.

Baseline results produced with different runner wrapper versions are not directly
comparable without an explicitly scoped rerun.

# CTX1 Compact Diagnostics Prompt Design - 2026-05-09

## Scope

CTX1 inspected the T1-style adaptive repair path in `runners/run_adaptive_repair.py` and prototyped a minimal, default-off compact diagnostics option for compile-only adaptive repair. This note is intentionally limited to prompt construction and risk assessment.

## Where T1 Prompts Are Built

The T1-style path is the compile-only adaptive repair mode in `run_adaptive_repair.py`:

- `run_task(...)` enters the T1-style branch when `args.compile_only_closure` is set.
- `_compile_plan_prompt(...)` builds the optional plan-only prompt used by `--compile-plan-execute`.
- `_compile_only_closure_prompt(...)` builds the repair execution prompt.
- Both prompts call `_compile_gate_score_summary(...)` to render the current validator status, scores, gate issues, concrete diagnostics, and verbose validator notes.
- The plan prompt is written to `adaptive_round*/repair_plan_prompt.md`; the execution prompt is written to `adaptive_round*/repair_prompt.md`.

The smallest useful insertion point is `_compile_gate_score_summary(...)` because it is shared by both plan and execution prompts and does not affect scoring, candidate selection, model calling, artifact extraction, or EVAS validation.

## Implemented Prototype

A default-off CLI flag was added:

```bash
--compile-compact-diagnostics
```

Behavior:

- Requires `--compile-only-closure`.
- Leaves all existing runs unchanged when omitted.
- Threads `compact_diagnostics` into `_compile_plan_prompt(...)` and `_compile_only_closure_prompt(...)`.
- When enabled, `_compile_gate_score_summary(..., compact=True)` keeps:
  - current validator status,
  - current gate layer,
  - gate-cleared boolean,
  - one-line score tuple,
  - gate issues,
  - concrete diagnostics from `_concrete_diagnostics(result)`.
- It drops the verbose `Validator notes:` block from this summary only. The rest of the prompt still includes syntax-zero policy, compile history, optional routed compile skills, optional context-engineering capsule, mechanism guidance, public task prompt, and candidate files.

## Minimum Patch Shape

The minimum code change is:

1. Add `compact: bool = False` to `_compile_gate_score_summary(...)`.
2. Add a compact rendering branch before the existing verbose rendering.
3. Add `compact_diagnostics: bool` parameters to `_compile_plan_prompt(...)` and `_compile_only_closure_prompt(...)`.
4. Pass `args.compile_compact_diagnostics` from `_run_compile_plan_step(...)` and the compile-only repair branch in `run_task(...)`.
5. Add `--compile-compact-diagnostics` to argparse and require `--compile-only-closure`.
6. Record `compile_compact_diagnostics` in round/final metadata and summary condition flags.

This is backward-compatible because every new path defaults to `False` and the old prompt text is preserved byte-for-byte for default calls except for function signatures and metadata fields when the flag exists but is false.

## Validation Commands Run

From `behavioral-veriloga-eval/`:

```bash
python3 -m py_compile runners/run_adaptive_repair.py
python3 runners/run_adaptive_repair.py --help | rg -n "compile-compact-diagnostics|compile-plan-execute|compile-only-closure" -C 2
python3 runners/run_adaptive_repair.py --compile-compact-diagnostics --task dwa_ptr_gen_no_overlap_smoke 2>&1 | head -5
```

Observed:

- Python syntax check passed.
- Help text includes `--compile-compact-diagnostics`.
- Guard check prints `--compile-compact-diagnostics requires --compile-only-closure` when the flag is used outside compile-only mode.

## Risks

- Prompt-behavior risk: compact mode removes the full validator notes from the score summary, so the model may miss a useful raw note that was not captured by `_concrete_diagnostics(...)` or gate issues.
- Mitigation: compact mode is default-off and compile-only-gated; it should first be evaluated on the T1 residual compile slice before broader use.
- Coverage risk: no live LLM/EVAS run was executed in CTX1; validation only checked syntax, CLI exposure, and flag gating.
- Interaction risk: with `--compile-context-engineering`, some structured diagnostic atoms still depend on raw notes and remain available in the context capsule, reducing risk. Without CE, compact mode is more aggressive.

## Suggested T1 Smoke Command

Use an isolated generated/results root and the known T1 residual tasklist or slice. Example shape:

```bash
python3 runners/run_adaptive_repair.py \
  --bench-dir benchmark-vabench-main-v1 \
  --model mimo-v2.5-pro \
  --compile-only-closure \
  --compile-plan-execute \
  --compile-context-engineering \
  --compile-compact-diagnostics \
  --max-rounds 2 \
  --patience 1 \
  --generated-root generated-ctx1-compactdiag-t1-smoke-20260509 \
  --output-root results/ctx1-compactdiag-t1-smoke-20260509 \
  --task <task_id>
```

For a fair ablation, compare prompt character/token counts and compile-closure outcome against the same command without `--compile-compact-diagnostics`.

---
name: vabench-review-sop
description: Review vaBench benchmark-v3 tasks with a self-contained two-gate SOP. Use when auditing task independence, prompt hygiene, public/hidden artifact boundaries, checker alignment, negative variants, Cadence/Spectre modeling quality, AHDL lint status, EVAS compatibility issues, or PR readiness for benchmark task changes.
---

# vaBench Review SOP

## Overview

Use this skill to apply a self-contained two-gate review process to vaBench
tasks. The complete SOP is bundled inside this skill at
`references/two-gate-sop.md`; do not depend on a separate repository SOP file.

## Required Reference

For formal benchmark audits, prompt/gold repairs, scoring/admission decisions,
or PR preparation, read `references/two-gate-sop.md` completely before acting.
For lightweight questions about the skill itself, read only the relevant
section. If the bundled reference is missing, stop and report that the skill is
broken rather than inventing a replacement checklist.

## Workflow

1. Identify the task directories, related PR/issue scope, and any prior audit
   notes. Fetch upstream before changing files if a PR will be opened.
2. Apply Gate 1 first: function boundary, admission/counting label, artifact
   target/support boundary, visible-vs-hidden evaluation alignment, checker
   role, and negative-variant strength.
3. Apply Gate 2 only after Gate 1 is understood: prompt contract, gold
   Verilog-A modeling quality, metadata/checker/linter readiness, and actual
   Cadence/Spectre evidence.
4. If review exposes a valid EVAS parser/simulator/checker compatibility issue,
   stop benchmark-side admission work long enough to reduce and fix or open the
   EVAS upstream issue/PR. Do not hide an EVAS defect with a benchmark-only
   workaround.
5. Before editing prompts or gold artifacts, state the concrete issue being
   repaired and cite the task files or prompt lines that expose it. If the user
   asked for manual prompt review, list each proposed prompt issue and wait for
   human confirmation before changing benchmark assets, unless the user
   explicitly authorizes batch repair.
6. After changes, rerun the smallest checks that prove the claim: prompt hygiene
   scans, JSON/script validation, EVAS smoke where relevant, and
   Cadence/Spectre hidden/gold/negative slices when the status depends on them.

## Output Contract

For each reviewed task or group, report:

- Gate 1 admission/counting label and why.
- Gate 2 Cadence modeling-quality status and why.
- Prompt hygiene findings, especially public/private boundary leaks.
- Artifact boundary findings for `task.toml`, `starter`, `solution`, visible
  tests, hidden tests, and support files.
- Checker alignment and what behavior the checker actually proves.
- Negative variants run or missing, and whether failures are behavioral rather
  than syntax/setup failures.
- EVAS, AHDL lint, and Cadence/Spectre evidence, including any blockers.
- Concrete repair recommendations, separated from uncertain questions that need
  human review.

## Common Local Commands

Use these only when the corresponding files exist in the current workspace:

- Regenerate issue29 duplicate/filler report:
  `python3 benchmark-vabench-release-v3/scripts/audit_issue29_duplicates.py`
- Run v3 gold smoke for a task range:
  `PYTHONPATH=runners python3 scripts/run_v3_gold_smoke_range.py --start <N> --end <N> --out <file.json>`
- Run Spectre audit for a task:
  `python3 scripts/run_v3_spectre_audit.py --task <task-dir> --split hidden --timeout-s 300 --work-root <dir> --out <file.json>`
- Run Spectre negative variants:
  `python3 scripts/run_v3_spectre_audit.py --task <task-dir> --split hidden --all-negative-variants --timeout-s 300 --work-root <dir> --out <file.json>`
- Validate generated JSON:
  `python3 -m json.tool <file.json>`
- Check Python audit scripts:
  `PYTHONPYCACHEPREFIX=/private/tmp/vaevas-pycache python3 -m py_compile <script.py>`

## Guardrails

- Keep `task.toml` form separate from benchmark admission status.
- Do not promote EVAS pass evidence alone to `cadence_modeling_ready` when
  Cadence evidence or AHDL lint is expected but missing.
- Do not mention hidden evaluator/checker internals in public prompts. Use
  public boundary wording such as checker logic, private test hooks, or
  simulator-private side channels.
- Treat visible testbenches as public verification scenarios for DUT tasks, not
  as values the DUT should hard-code unless the prompt explicitly makes the
  value part of the public contract.
- Keep support components, Measurement L2 flows, Core Circuit L2 flows, and
  standalone L1 functions distinct in reports and PR descriptions.
- Preserve user-requested manual review checkpoints; do not silently convert a
  prompt-review question into unrelated simulator-failure repair work.
- Keep skill/process updates separate from benchmark asset fixes. A skill-only
  PR should not mix in task prompt, gold, checker, or report repairs; benchmark
  asset PRs should edit the skill only when the review process itself changes.

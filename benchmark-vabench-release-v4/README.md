# vaBench Release v4 Pilot

This package is a 10-task v4 pilot surface for prompt, wrapper, and feedback-loop discussion. It does not replace or modify `benchmark-vabench-release-v3`.

## Scope

- 10 tasks copied from current v3 core score-candidate tasks.
- Clean canonical `instruction.md` files with task contract, public interface, public parameters, required behavior, modeling constraints, and output contract.
- G0-G5 prompt-mode wrappers in `prompt_modes/`.
- Public feedback-oracle runners for agentic EVAS feedback.
- Public feedback TBs exposed only to agentic feedback runs.
- Private score TBs, checker profiles, gold solutions, and negative variants kept evaluator-only.
- Local report generators and audits for prompt rendering, experiment records, runner ingestion, feedback strength, and package integrity.

Generated reports under `reports/` are intentionally ignored by git. Recreate them with the maintenance commands below when reviewing or running the pilot.

## Pilot Tasks

- `001-bang-bang-phase-detector`
- `007-first-order-lowpass`
- `010-offset-comparator`
- `013-resettable-integrator`
- `014-sar-logic`
- `017-slew-rate-limiter`
- `021-vco-phase-integrator`
- `026-clocked-sample-and-hold`
- `029-dwa-dem-encoder`
- `040-programmable-gain-amplifier`

## Prompt Policy

Canonical task prompts must describe only the public task contract:

- target artifact names;
- module names, positional port order, and electrical interface;
- public parameter defaults and override semantics;
- observable behavior required from the DUT;
- modeling constraints that are part of the public deliverable;
- exact output artifact contract.

Canonical task prompts must not contain runner or evaluator mechanics such as feedback-oracle profile paths, score `.scs` decks, EVAS permission, private score mechanics, validation sample windows, transient stop times, Vela paths, or private evaluator instructions. Benchmark classification metadata such as form, level, and category belongs in `TASKS.json`, not in solver-facing prompts.

## Prompt Modes

- `G0`: direct baseline; canonical task prompt only, no tools and no feedback oracle.
- `G1`: direct one-shot plus a generic Verilog-A writing checklist; no tools and no feedback oracle.
- `G2`: agent loop with the visible feedback oracle and no additional Verilog-A or feedback/debug skill wrapper.
- `G3`: agent loop with the visible feedback oracle plus the generic Verilog-A writing checklist.
- `G4`: agent loop with the visible feedback oracle plus a generic feedback/debug skill for using oracle diagnostics.
- `G5`: agent loop with the visible feedback oracle plus both the Verilog-A writing checklist and the feedback/debug skill.

The reusable skill texts live under `prompt_modes/skills/` and are referenced by rendered prompt metadata and experiment records with SHA-256 hashes.

See `prompt_modes/g0_g5_mode_discussion.md` for the full mode definitions, boundaries, and recommended comparisons.

In agentic modes, feedback includes any AHDL-like preflight or lint-style diagnostics emitted by the feedback oracle. This is part of the EVAS-backed feedback channel, not a separate gate or a separate mode.

## Oracle Layout

Each task uses this public/private boundary:

- model-visible files: `instruction.md`, `public_contract.json`, `test_feedback/public_tb.scs`, and `test_feedback/run_feedback.py`;
- evaluator-only files: `solution/`, `evaluator/score_tb.scs`, `evaluator/checker_profile.json`, `evaluator/run_score.py`, and `negative_variants/`;
- no task keeps a model-visible `starter/` directory;
- the public feedback TB is the only TB exposed to agentic runs;
- the private score TB is used only for final scoring;
- checker binding and trace contract live in `evaluator/checker_profile.json`, not inside TB files.

The feedback oracle is queryable by agentic modes through:

```bash
VABENCH_FEEDBACK_SOURCE_DIR=<candidate-dir> python3 test_feedback/run_feedback.py
```

The public feedback TB is a debugging example and the only TB used by the feedback loop. The private score TB is a same-contract held-out deck: it should vary numeric stimuli, timing, corners, or coverage strength, not define a second task. The private score TB and checker profile are evaluator-only and not queryable by agentic modes.

## Experiment Specs

`scripts/generate_experiment_specs.py` materializes traceable run records for each task/mode pair:

- `G0` and `G1` are direct `llms` records.
- `G2`, `G3`, `G4`, and `G5` are `agents` records.
- direct records expose no shell, no file browsing, and no feedback oracle.
- agentic records expose only the feedback surface, public feedback TB, and the feedback command.
- agentic records expose structured EVAS feedback channels: `ahdl_like_preflight`, `evas_simulation`, and `behavior_property_diagnostics`.
- private score assets are never exposed by any mode.

`scripts/audit_experiment_specs.py` checks that the generated records match these mode policies and that prompt hashes match the renderer.

## Runner Ingestion

`scripts/materialize_runner_jobs.py` consumes `reports/experiment_specs/records.jsonl` and writes one runner-side dry-run job per record under `reports/runner_ingestion/`. The job manifest preserves record fingerprints, prompt hashes, process families, skills, access policies, feedback surface mounts, and allowed commands. `scripts/audit_runner_ingestion.py` compares the jobs back to the source records and fails if the runner-side view drifts.

This proves the v4 pilot has a concrete ingestion contract before costly model or agent execution. It does not claim that an external production Vela deployment has already run these jobs.

## Feedback Strength

`scripts/audit_feedback_strength.py` classifies feedback oracles as:

- `compile_only_smoke`: feedback runner checks compile/transient markers only.
- `light_behavior`: feedback runner appears to inspect traces or expected values, but no shared task checker id was found.
- `behavior_checked`: feedback runner invokes EVAS and a task-specific behavior checker.
- `missing_or_unknown`: missing runner/profile or unrecognized shape.

The audit also classifies checker level. The v4 pilot expects all selected tasks to be `behavior_checked` and to resolve to a registered feedback checker with an effective trace-signal contract.

## Maintenance Commands

Use these commands after changing v4 tasks or wrappers:

```bash
python3 benchmark-vabench-release-v4/scripts/render_prompt_modes.py --mode all --out-dir reports/rendered_prompts
python3 benchmark-vabench-release-v4/scripts/generate_experiment_specs.py
python3 benchmark-vabench-release-v4/scripts/materialize_runner_jobs.py
python3 benchmark-vabench-release-v4/scripts/audit_feedback_strength.py
python3 benchmark-vabench-release-v4/scripts/audit_experiment_specs.py
python3 benchmark-vabench-release-v4/scripts/audit_runner_ingestion.py
python3 benchmark-vabench-release-v4/scripts/audit_v4_pilot.py
```

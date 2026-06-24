# Agentic EVAS Ablation Plan

This document defines a controlled experiment for measuring whether visible
EVAS simulation and Verilog-A authoring skills improve model performance on the
Behavioral Verilog-A DUT benchmark.

## Goal

We want to separate three effects:

1. Whether the agent can improve solutions by running visible/public EVAS
   simulations before submitting.
2. Whether a Verilog-A writer skill improves direct code generation even when
   no local simulation is allowed.
3. Whether an EVAS simulation skill helps the agent actually use visible
   simulation effectively.

Hidden scoring must stay identical across all groups. The only intended
differences are the model-side prompt constraints and the skills attached to
the agent.

## Fixed Evaluation Setup

All groups should use:

- The same task set, initially the 49 DUT release slice.
- The same model.
- The same Docker image.
- The same hidden evaluator.
- The same scoring rubric.
- The same concurrency and run budget, unless a run is explicitly marked as a
  smoke run.
- The same hidden EVAS/Spectre-compatible checker path.

The hidden evaluator must run after the model submits its source patch. The
agent must never see hidden tests, hidden checkers, or hidden reference
solutions.

## Skills

Use two separate skills:

- `skills/veriloga_writer_skill.md`: how to write Verilog-A behavioral DUT
  modules.
- `skills/evas_sim_skill.md`: how to run EVAS visible/public simulation and
  inspect outputs.

Keep them separate. The writer skill should not teach simulation workflow. The
EVAS skill should not be treated as the main authoring guide.

## Five Experimental Groups

| Group | Writer Skill | EVAS Skill | Visible EVAS Allowed | Name |
|---|---:|---:|---:|---|
| G0 | no | no | no | Direct baseline |
| G1 | yes | no | no | Writer-skill direct |
| G2 | no | no | yes | Prompt-only visible EVAS |
| G3 | yes | no | yes | Writer + prompt visible EVAS |
| G4 | yes | yes | yes | Writer + EVAS-skill visible EVAS |

These five groups are intentionally not the full factorial matrix. We exclude
the less meaningful condition "EVAS skill present but visible EVAS forbidden",
because that turns a simulation skill into vague background knowledge and makes
results hard to interpret. We also exclude "EVAS skill without writer skill but
visible EVAS allowed" as a primary group because the intended product flow is
to teach both Verilog-A authoring and EVAS usage when allowing agentic
simulation.

## Prompt Policies

### No-Visible-EVAS Groups

Groups G0 and G1 must explicitly forbid local simulation:

```text
Do not run EVAS, Spectre, or any local simulator/test harness.
Do not try to reconstruct or execute hidden evaluation logic.
Directly edit the requested Verilog-A source artifact(s) and submit the source.
The hidden evaluator will run EVAS separately after submission.
```

### Visible-EVAS Groups

Groups G2, G3, and G4 should explicitly allow public simulation:

```text
You may use visible/public EVAS simulation to debug your solution.
Use only public files. Do not inspect, infer, or reconstruct hidden tests.
If a visible smoke runner exists, run it. Otherwise you may create a small
public sanity testbench.
After your visible checks pass, or after you decide further visible checking is
not useful, submit the requested source artifact(s).
The hidden evaluator will run separately after submission.
```

The visible-EVAS permission is a permission, not a requirement. The model may
choose not to run it. That behavior should be measured.

## Primary Comparisons

- `G1 - G0`: writer skill benefit under direct source generation.
- `G2 - G0`: visible EVAS permission benefit without any skill.
- `G3 - G1`: visible EVAS permission benefit when the writer skill is present.
- `G4 - G3`: EVAS skill benefit when visible EVAS is allowed.
- `G4 - G1`: full agentic visible-EVAS workflow benefit over writer-only direct
  generation.

## Required Metrics

For every group, report:

- Hidden reward average.
- Hidden pass count.
- Status distribution:
  - `PASS`
  - `FAIL_DUT_COMPILE`
  - `FAIL_TB_COMPILE`
  - `FAIL_SIM_CORRECTNESS`
  - platform/sandbox failures, if any
- Token usage.
- Cost.
- Wall-clock runtime.
- Per-task reward and status.

For visible-EVAS groups, additionally report:

- How many tasks actually invoked visible EVAS.
- Which command pattern was used:
  - `run_visible_smoke.py`
  - `evas simulate`
  - repository EVAS runner
  - custom public testbench
- Visible pass / hidden pass count.
- Visible pass / hidden fail count.
- Visible fail / hidden pass count.
- Tasks where the agent did not use visible EVAS despite being allowed.

## Model-Log Audit

After each run, inspect model logs to verify the intended condition:

- G0/G1 should have no model-side commands matching:
  - `evas`
  - `spectre`
  - `simulate_evas`
  - `run_visible_smoke`
  - `score_task`
  - `pytest`
  - `python3`
  - `python`
- G2/G3/G4 should be checked for actual visible-EVAS usage, not only for the
  prompt saying EVAS is allowed.
- Hidden evaluator EVAS runs are separate and should be identified from
  evaluator score notes, not model logs.

The important distinction is:

- Model-side visible EVAS: optional agentic reasoning signal.
- Hidden-side EVAS: mandatory final scoring signal.

Do not conflate the two.

## Execution Plan

### Stage 1: Smoke Run

Run all five groups on the same 10-task smoke subset.

Acceptance criteria before full 49-task runs:

- All five groups complete without platform-level failure.
- G0/G1 model logs show no local simulation commands.
- At least one of G2/G3/G4 shows actual visible-EVAS usage. If none of them
  uses EVAS, improve the visible-EVAS prompt or skill before the full run.
- Hidden evaluator outputs are present for all groups.

### Stage 2: Full DUT49 Run

Run all five groups on the 49 DUT release slice.

Use the same task ordering and same hidden evaluator for all groups. If image
tags or process snippets change between groups, discard the comparison and
rerun under a consistent configuration.

### Stage 3: Report

Produce a single comparison report with:

- Headline metrics table for all five groups.
- Per-task matrix: reward/status by group.
- Model-side EVAS usage table for G2/G3/G4.
- Failure taxonomy.
- Cost and runtime comparison.
- Conclusions for the primary comparisons listed above.

## Interpretation Rules

If G2 improves over G0, then prompt-only permission to use visible EVAS may be
enough for the model to benefit.

If G4 improves over G3, then the EVAS skill likely helps the agent use visible
simulation better.

If G3 improves over G1, then visible EVAS helps when the model already has
Verilog-A writing guidance.

If G1 improves over G0, then the writer skill helps direct code quality even
without local validation.

If visible pass / hidden fail is high, visible smoke tests are too weak or too
misaligned with hidden scoring. This should trigger task-level visible-test
improvement, not hidden-check weakening.

If visible EVAS is allowed but rarely used, improve the prompt, skill, or
workspace affordances so the agent can find and run the visible tests.

## Reporting Discipline

Always report whether each group actually used model-side EVAS. Do not infer
agentic reasoning from the presence of an EVAS skill alone.

Always keep hidden EVAS scoring identical across groups. Any change to the
hidden evaluator, image contents, process snippet, or task set invalidates a
cross-group comparison unless all groups are rerun.

# vaBench Submission Contract

Complete only the candidate artifacts declared by the task. Preserve exact
file names and do not emit evaluator, score, or self-reported PASS/FAIL files.
Every declared `target_artifacts` path is relative to the submission root; do
not add an undeclared common directory around the bundle.

In direct one-shot mode, emit only the final artifact bundle: do not emit
analysis, preliminary versions, drafts, revisions, or explanatory text. Return
each candidate exactly once inside
`<<<VABENCH_ARTIFACT path="...">>>` and `<<<END_VABENCH_ARTIFACT>>>` markers,
with no text outside the artifact blocks. In agentic mode, inspect the mounted
public task inputs and write only the final candidate files under
`public/submission/`. Feedback tools, when available, are diagnostic only; the
private Spectre score is not exposed.

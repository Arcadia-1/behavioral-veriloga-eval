# vaBench Agentic Submission Contract

Inspect the mounted public task inputs and write only the final candidate
artifacts under `public/submission/`. Preserve exact file names, module names,
ports, parameters, and required artifact paths.

The public task mount contains a transparent EVAS runtime package. Invoke
`evas` directly against its visible test and keep generated output under
`/tmp/vabench-visible/`. Do not emit evaluator, score, debug-only, simulator
output, fixture links, or self-reported PASS/FAIL files as candidate artifacts.

# vaBench Direct Submission Contract

Return only the candidate artifacts declared by the task. Preserve exact file
names, module names, ports, parameters, and required artifact paths.

For each candidate file, emit the complete file contents exactly once inside
`<<<VABENCH_ARTIFACT path="...">>>` and
`<<<END_VABENCH_ARTIFACT>>>` markers. Do not include explanatory prose,
diagnostic logs, pass/fail claims, or undeclared files outside the artifact
blocks.

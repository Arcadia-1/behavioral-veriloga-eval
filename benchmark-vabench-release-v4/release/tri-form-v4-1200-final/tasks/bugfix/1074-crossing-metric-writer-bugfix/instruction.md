# Crossing Metric Writer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `file_metric_writer.va`: `file_metric_writer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FILE_OPEN`: The filename parameter names exactly one metric file basename in the runner-provided writable working directory; absolute paths and directory traversal are outside the public contract.
- `P_FIRST_RISING_CROSSING`: The first rising crossing of vin through vth is the event that records the metric and latches completion.
- `P_RECORDED_TIME`: The metric file contains exactly one text record of the form `cross <time_seconds>` followed by a newline, where <time_seconds> is the first rising crossing time.
- `P_DONE_LATCH`: done remains low before the first qualifying crossing and high after it, with transition smoothing set by tr.
- `P_SINGLE_RECORD`: Later vin crossings do not clear done or create additional metric records.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `file_metric_writer.va`.
Every supplied `.va` file is editable; do not add or omit files.

# Crossing Metric Writer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `file_metric_writer.va`: `file_metric_writer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_FILE_OPEN`: The filename parameter names exactly one metric file basename in the runner-provided writable working directory; absolute paths and directory traversal are outside the public contract.
- `P_FIRST_RISING_CROSSING`: The first rising crossing of vin through vth is the event that records the metric and latches completion.
- `P_RECORDED_TIME`: The metric file contains exactly one text record of the form `cross <time_seconds>` followed by a newline, where <time_seconds> is the first rising crossing time.
- `P_DONE_LATCH`: done remains low before the first qualifying crossing and high after it, with transition smoothing set by tr.
- `P_SINGLE_RECORD`: Later vin crossings do not clear done or create additional metric records.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `file_metric_writer.va`.
Do not add or omit artifacts.

# Non-overlapping Clock Generator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `nonoverlap_clock_generator.va`: `nonoverlap_clock_generator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_OR_A_LOW_ENABLE_CLEARS`: Reset or a low `enable` clears both phases, `deadtime_metric`, and `valid`.
- `P_A_RISING_CLK_IN_REQUEST_EVENTUALLY`: A rising `clk_in` request eventually enables `phi1`; a falling `clk_in` request eventually enables `phi2`.
- `P_DURING_EACH_HANDOFF_BOTH_PHI1_AND`: During each handoff, both `phi1` and `phi2` remain low for the configured dead-time interval.
- `P_PHI1_AND_PHI2_MUST_NEVER_BE`: `phi1` and `phi2` must never be high at the same time.
- `P_DEADTIME_METRIC_IS_HIGH_ONLY_WHILE`: `deadtime_metric` is high only while a pending phase request is in the enforced both-low interval.
- `P_VALID_BECOMES_HIGH_AFTER_THE_FIRST`: `valid` becomes high after the first enabled handoff completes and remains high until reset or disable.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `nonoverlap_clock_generator.va`.
Every supplied `.va` file is editable; do not add or omit files.

# Comparator Delay Overdrive Meter Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `comparator_delay_overdrive_meter.va`: `comparator_delay_overdrive_meter`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CLOCK_ARMED_MEASUREMENT`: Each rising `clk` threshold crossing stores the launch time, captures absolute differential overdrive, and arms exactly one pending measurement.
- `P_DECISION_DELAY_CAPTURE`: The first qualifying `outp` or `outn` decision edge while armed reports the elapsed clock-to-decision delay in `delay_ps`.
- `P_ABSOLUTE_OVERDRIVE_METRIC`: `overdrive_mv` reports the absolute input differential magnitude at launch time.
- `P_POLARITY_AND_VALID_FLAG`: `polarity` reports the winning output decision direction and `valid` asserts only for a completed armed measurement.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `comparator_delay_overdrive_meter.va`.
Every supplied `.va` file is editable; do not add or omit files.

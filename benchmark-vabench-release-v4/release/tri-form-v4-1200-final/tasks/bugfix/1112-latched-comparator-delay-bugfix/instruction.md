# Latched Comparator Delay Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `latched_comparator_delay.va`: `latched_comparator_delay`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SUPPLY_REFERENCED_THRESHOLD`: The latch clock threshold is the midpoint of VDD and GND, and DOUT low and high levels use those same rails.
- `P_RISING_EDGE_LATCH`: Each rising CLK midpoint crossing latches one comparison result; falling crossings do not resample the input.
- `P_OFFSET_DECISION`: With vn zero, DOUT latches high exactly when VINP minus VINN exceeds vos and low otherwise.
- `P_SEEDED_RANDOM_TERM`: With vn nonzero, each latch decision includes a normal input-referred term scaled by vn from the sequence initialized by seed_init.
- `P_INTEREDGE_HOLD`: The latched decision holds between rising CLK events even if VINP or VINN changes.
- `P_DELAY_AND_SMOOTHING`: DOUT applies td delay and tr transition smoothing after each latch event.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `latched_comparator_delay.va`.
Every supplied `.va` file is editable; do not add or omit files.

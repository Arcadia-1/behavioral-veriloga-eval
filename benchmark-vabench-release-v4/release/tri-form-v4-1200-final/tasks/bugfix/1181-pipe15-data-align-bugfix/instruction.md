# Pipe15 Data Align Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pipe15_data_align.va`: `pipe15_data_align`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SAMPLE_ON_RISING_SAMP`: On each rising `samp` crossing, sample all fifteen input bits `d0..d14` into the alignment pipeline.
- `P_ZERO_DELAY_OUTPUT_GROUP`: Outputs `do0..do2` publish the current sampled values without an added sample delay.
- `P_STAGGERED_DELAY_OUTPUT_GROUPS`: Outputs `do3..do6`, `do7..do10`, and `do11..do14` publish the one-, two-, and three-sample delayed input groups respectively.
- `P_VOLTAGE_CODED_OUTPUT_LEVELS`: Every aligned output is driven as a voltage-coded logic level near 0 V or `vdd` with the declared transition timing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pipe15_data_align.va`.
Every supplied `.va` file is editable; do not add or omit files.

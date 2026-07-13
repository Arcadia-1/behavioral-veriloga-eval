# Digitally Controlled Delay Cell Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `digitally_controlled_delay_cell.va`: `digitally_controlled_delay_cell`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_CLEAR`: Reset clears the loaded code state, delayed clock, delay metric, valid indication, and pending edges.
- `P_CODE_CAPTURE_METRIC`: A rising load edge captures the six-bit unsigned code and the delay metric reports the normalized captured code.
- `P_EDGE_DELAY_MAPPING`: Each input-clock edge appears at the output after delay_min plus delay_lsb times the code captured for that edge.
- `P_PULSE_INTEGRITY_VALID`: Rising and falling edges receive equal delay, preserving pulse width, and valid asserts after the first delayed rising edge.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `digitally_controlled_delay_cell.va`.
Every supplied `.va` file is editable; do not add or omit files.

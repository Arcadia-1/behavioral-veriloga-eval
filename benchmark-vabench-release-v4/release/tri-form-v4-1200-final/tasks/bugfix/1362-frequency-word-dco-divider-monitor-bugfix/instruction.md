# Frequency-word DCO with Divider Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `frequency_word_dco.va`: `frequency_word_dco`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_STOP`: Reset or disabled operation stops and clears both clocks, the divider counter, and the frequency metric.
- `P_FREQUENCY_WORD_MAPPING`: The six-bit frequency word maps to min(f_max, f_min plus f_step times code), with the public normalized metric matching that target.
- `P_DIVIDER_MONITOR`: div_clk toggles once per divide_ratio rising DCO edges and its counter restarts after reset or disable.
- `P_RESTART_MONOTONICITY`: Enable restarts both clocks low with the first DCO rise one half-period later, and larger frequency words produce nondecreasing edge counts.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `frequency_word_dco.va`.
Every supplied `.va` file is editable; do not add or omit files.

# Switched-cap Phase Sequencer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `hold_flagger.va`: `hold_flagger`
- `nonoverlap_phase_gen.va`: `nonoverlap_phase_gen`
- `sample_switch_scheduler.va`: `sample_switch_scheduler`
- `switched_cap_phase_seq_top.va`: `switched_cap_phase_seq_top`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation clears all phase outputs, commands, phase code, and valid.
- `P_ONE_HOT_SEQUENCE`: Enabled rising clock edges advance cyclically through four one-hot phases with no overlapping high phases.
- `P_COMMAND_MAPPING`: sample_cmd is high exactly for phi1 or phi2, while hold_cmd is high exactly for phi3 or phi4.
- `P_PHASE_CODE`: phase_code_1 and phase_code_0 encode the active phase index zero through three.
- `P_VALID_AFTER_SEQUENCE`: valid remains low initially and asserts only after a complete enabled four-phase sample/hold sequence.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `hold_flagger.va`, `nonoverlap_phase_gen.va`, `sample_switch_scheduler.va`, `switched_cap_phase_seq_top.va`.
Every supplied `.va` file is editable; do not add or omit files.

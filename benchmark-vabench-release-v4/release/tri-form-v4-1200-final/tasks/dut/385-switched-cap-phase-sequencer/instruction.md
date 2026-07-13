# Switched-cap Phase Sequencer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `hold_flagger.va`: `hold_flagger`
- `nonoverlap_phase_gen.va`: `nonoverlap_phase_gen`
- `sample_switch_scheduler.va`: `sample_switch_scheduler`
- `switched_cap_phase_seq_top.va`: `switched_cap_phase_seq_top`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation clears all phase outputs, commands, phase code, and valid.
- `P_ONE_HOT_SEQUENCE`: Enabled rising clock edges advance cyclically through four one-hot phases with no overlapping high phases.
- `P_COMMAND_MAPPING`: sample_cmd is high exactly for phi1 or phi2, while hold_cmd is high exactly for phi3 or phi4.
- `P_PHASE_CODE`: phase_code_1 and phase_code_0 encode the active phase index zero through three.
- `P_VALID_AFTER_SEQUENCE`: valid remains low initially and asserts only after a complete enabled four-phase sample/hold sequence.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `hold_flagger.va`, `nonoverlap_phase_gen.va`, `sample_switch_scheduler.va`, `switched_cap_phase_seq_top.va`.
Do not add or omit artifacts.

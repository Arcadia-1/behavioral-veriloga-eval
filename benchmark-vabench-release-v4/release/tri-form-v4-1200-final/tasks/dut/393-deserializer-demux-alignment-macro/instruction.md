# Deserializer DEMUX Alignment Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `deserializer_demux_alignment_macro.va`: `deserializer_demux_alignment_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear all parallel outputs, `phase_metric`, and `word_valid`.
- `P_A_RISING_ALIGN_PULSE_RESETS_THE`: A rising `align_pulse` resets the slot pointer so the next sampled serial bit is written to `out0`.
- `P_ON_EACH_RISING_CLK_EDGE_WHILE`: On each rising `clk` edge while enabled, sample `serial_in` into the active output slot and advance the slot pointer.
- `P_ASSERT_WORD_VALID_AFTER_ALL_FOUR`: Assert `word_valid` after all four output slots have been updated since the most recent alignment event.
- `P_PHASE_METRIC_MUST_EXPOSE_THE_ACTIVE`: `phase_metric` must expose the active slot pointer.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `deserializer_demux_alignment_macro.va`.
Do not add or omit artifacts.

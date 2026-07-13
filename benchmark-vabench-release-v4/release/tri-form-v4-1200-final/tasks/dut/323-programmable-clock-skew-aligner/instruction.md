# Programmable Clock Skew Aligner

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `programmable_clock_skew_aligner.va`: `programmable_clock_skew_aligner`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive output and metrics low.
- `P_DECODE_SKEW_2_SKEW_0_AS`: Decode `skew_2..skew_0` as a programmable output-edge delay code.
- `P_FOR_EACH_ACCEPTED_INPUT_CLOCK_EDGE`: For each accepted input clock edge, schedule one output edge after the code-dependent delay.
- `P_EXPOSE_THE_ACTIVE_DELAY_CODE_AS`: Expose the active delay code as `delay_metric`.
- `P_ASSERT_VALID_AFTER_THE_FIRST_DELAYED`: Assert `valid` after the first delayed output edge has been generated.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `programmable_clock_skew_aligner.va`.
Do not add or omit artifacts.

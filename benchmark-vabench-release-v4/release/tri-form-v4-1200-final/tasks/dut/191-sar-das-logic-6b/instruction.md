# SAR DAS Logic 6b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `sar_das_logic_6b.va`: `sar_das_logic_6b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SAMPLING_RESET_CONVERSION_STATE`: A rising `clk_sampling` transition clears controls and pulses, and a falling transition arms the SAR conversion sequence.
- `P_SAR_COMPARATOR_POLARITY`: Each rising `clk_sar` transition compares `vcomp` to `vcm` and drives `co/cob` with the declared polarity.
- `P_SIX_BIT_DECISION_SEQUENCE`: The SAR decisions update `d6..d1` in the declared order through the conversion.
- `P_CONTROL_OUTPUT_LEVELS`: Decision pulses and bit-control outputs use valid voltage-coded low/high levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `sar_das_logic_6b.va`.
Do not add or omit artifacts.

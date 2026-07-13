# I/Q Upconversion Mixer Chain

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `iq_upconversion_mixer.va`: `iq_upconversion_mixer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation drives RF and debug outputs to vcm and clears quad_ok.
- `P_IQ_SIGNED_MIXING`: I and Q debug outputs equal vcm plus the specified signed LO products, including the negative Q-path convention.
- `P_RF_SUM_CLAMP`: rf_out equals the bounded sum of the I and Q path contributions about vcm.
- `P_QUADRATURE_ACTIVITY`: quad_ok asserts only after each LO input has crossed threshold since the latest reset or enable event.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `iq_upconversion_mixer.va`.
Do not add or omit artifacts.

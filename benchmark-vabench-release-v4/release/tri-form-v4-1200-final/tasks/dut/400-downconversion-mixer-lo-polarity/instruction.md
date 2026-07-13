# Downconversion Mixer with LO Polarity

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `downconversion_mixer_lo_polarity.va`: `downconversion_mixer_lo_polarity`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CENTER`: Reset or disable centers I/Q outputs and clears LO metrics and polarity_ok.
- `P_LO_POLARITY_METRICS`: Each LO threshold state selects signed polarity and is mirrored by its public metric.
- `P_IQ_CONVERSION`: I and Q outputs follow the declared common-mode referenced conversion-gain equations with independent LO signs.
- `P_OUTPUT_CLAMP`: Both baseband outputs remain within the declared supply rails.
- `P_POLARITY_QUALIFICATION`: polarity_ok asserts only after both LO controls have toggled while enabled.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `downconversion_mixer_lo_polarity.va`.
Do not add or omit artifacts.

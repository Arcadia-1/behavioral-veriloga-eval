# IQ Downconversion Chain

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `iq_downconversion_chain.va`: `iq_downconversion_chain`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_COMMON_MODE`: Active-high reset returns I/Q baseband outputs, LO monitors, and mixer monitors to 0.45 V and phase_mon to 0.9 V.
- `P_QUADRATURE_SEQUENCE`: Successive non-reset rising clk edges cycle the I/Q coefficient pairs through (1,0), (0,1), (-1,0), and (0,-1), then wrap.
- `P_LO_MONITORS`: Lo_i and lo_q equal 0.45 V plus 0.40 V times their current quadrature coefficients.
- `P_MIXER_MONITORS`: Each mixer monitor equals 0.45 V plus 1.25 times the vin deviation times its LO coefficient, clamped to 0.02 V through 0.88 V.
- `P_BASEBAND_UPDATES`: On each valid edge, out and metric apply the public 0.85 first-order update toward mix_i and mix_q respectively and remain clamped to 0.02 V through 0.88 V.
- `P_PHASE_MONITOR`: Phase_mon exposes the current four-state phase as phase/3 times 0.9 V.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `iq_downconversion_chain.va`.
Do not add or omit artifacts.

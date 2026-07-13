# Cyclic Decoder 10b

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cyclic_decoder_10b.va`: `cyclic_decoder_10b`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_READY_SERIAL_CAPTURE`: After each publication clock, rising `ready` crossings collect up to `nbit` serial decisions MSB first.
- `P_TERNARY_WEIGHTING`: For each collected decision, high `dp` adds the full current binary weight and low `dp` with high `dn` adds half of that weight.
- `P_NORMALIZED_MIDSCALE_OUTPUT`: The decoded value is normalized by the public bit depth and shifted by the required midscale offset before driving `dout`.
- `P_CLOCKED_PUBLICATION_HOLD`: `dout` updates from event-driven ready/publication handling and holds between publication events.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cyclic_decoder_10b.va`.
Do not add or omit artifacts.

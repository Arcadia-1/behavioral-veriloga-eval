# Two Channel Sample Demux

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `two_channel_sample_demux.va`: `two_channel_sample_demux`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_CHANNEL_SELECTION`: A rising `clks1` crossing samples `samp1` and a rising `clks2` crossing samples `samp2` into the shared held output.
- `P_BOTH_CHANNELS_REACHABLE`: Both clocked sample channels can independently update `vout` without one channel masking the other.
- `P_OUTPUT_GAIN_AND_HOLD`: `vout` holds the selected sample amplitude without gain scaling between clock events.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `two_channel_sample_demux.va`.
Do not add or omit artifacts.

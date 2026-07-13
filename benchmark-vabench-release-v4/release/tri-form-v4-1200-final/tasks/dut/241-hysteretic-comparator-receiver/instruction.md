# Hysteretic Comparator Receiver

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `hysteretic_comparator_receiver.va`: `hysteretic_comparator_receiver`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_DEFINE_UPPER_TH_OFFSET_VHYS_2`: Define `upper_th = offset + vhys/2` and `lower_th = offset - vhys/2`. On initialization, set the output state high if `V(inp,inm)` is at or above the upper threshold; otherwise set it low. After initialization, switch high only on a rising crossing of `upper_th`, switch low only on a falling crossing of `lower_th`, and hold the previous state inside the hysteresis band. Drive `out` to the selected rail with delay `td` and transition time `tr`.
- `P_VOUT_HIGH_0_9_V_HIGH`: `vout_high = 0.9 V`: high output rail.
- `P_VOUT_LOW_0_0_V_LOW`: `vout_low = 0.0 V`: low output rail.
- `P_OFFSET_0_0_V_INPUT_REFERRED`: `offset = 0.0 V`: input-referred switching offset.
- `P_VHYS_40_MV_FROM_0_INF`: `vhys = 40 mV from [0:inf)`: total hysteresis width.
- `P_TD_400_PS_FROM_0_INF`: `td = 400 ps from [0:inf)`: propagation delay from a qualifying threshold crossing to the output state change.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `hysteretic_comparator_receiver.va`.
Do not add or omit artifacts.

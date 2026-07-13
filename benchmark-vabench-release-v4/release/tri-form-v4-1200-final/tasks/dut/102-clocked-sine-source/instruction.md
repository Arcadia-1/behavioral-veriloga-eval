# Clocked Sine Source

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `vin_src.va`: `vin_src`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_COMMON_MODE`: While RST_N is below vth, both outputs hold near vdd divided by two.
- `P_RISING_EDGE_SAMPLE`: After reset release, VOUT_P updates only on rising CLK crossings through vth.
- `P_SAMPLED_SINE`: At each qualifying clock edge, VOUT_P samples vdd/2 plus ampl times sin(2*pi*freq*time), plus the optional seeded perturbation.
- `P_REFERENCE_SIDE_COMMON_MODE`: VOUT_N remains at vdd divided by two during reset and active sampling.
- `P_INTEREDGE_HOLD`: Both outputs hold their sampled values between CLK events rather than continuously recomputing the sine or perturbation.
- `P_SEEDED_REPEATABILITY`: For fixed SEED, sigma, controls, and timing, the sampled perturbation sequence and outputs are repeatable; sigma zero removes the perturbation.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `vin_src.va`.
Do not add or omit artifacts.

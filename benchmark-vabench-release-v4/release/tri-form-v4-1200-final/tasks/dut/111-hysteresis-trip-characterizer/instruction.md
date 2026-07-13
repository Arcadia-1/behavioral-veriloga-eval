# Hysteresis Trip Characterizer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `hysteresis_trip_characterizer.va`: `hysteresis_trip_characterizer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SUPPLY_MIDPOINT_THRESHOLD`: The characterizer detects cmp_out transitions through the instantaneous midpoint of vdd and vss.
- `P_RISING_TRIP_CAPTURE`: On each rising cmp_out midpoint crossing, trip_rise captures the instantaneous vin minus vss value.
- `P_FALLING_TRIP_CAPTURE`: On each falling cmp_out midpoint crossing, trip_fall captures the instantaneous vin minus vss value.
- `P_LATEST_EDGE_REFRESH`: Later rising or falling transitions refresh the corresponding captured trip value rather than leaving only the first measurement.
- `P_HYSTERESIS_WIDTH_SIGN`: After both directions are captured, hyst_width equals trip_rise minus trip_fall with that signed polarity.
- `P_VALID_AFTER_BOTH_DIRECTIONS`: Valid remains at vss until at least one rising and one falling trip have been captured, then rises to vdd.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `hysteresis_trip_characterizer.va`.
Do not add or omit artifacts.

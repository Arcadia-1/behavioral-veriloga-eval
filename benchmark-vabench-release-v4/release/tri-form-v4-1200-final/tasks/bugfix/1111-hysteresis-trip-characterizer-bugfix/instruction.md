# Hysteresis Trip Characterizer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `hysteresis_trip_characterizer.va`: `hysteresis_trip_characterizer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_SUPPLY_MIDPOINT_THRESHOLD`: The characterizer detects cmp_out transitions through the instantaneous midpoint of vdd and vss.
- `P_RISING_TRIP_CAPTURE`: On each rising cmp_out midpoint crossing, trip_rise captures the instantaneous vin minus vss value.
- `P_FALLING_TRIP_CAPTURE`: On each falling cmp_out midpoint crossing, trip_fall captures the instantaneous vin minus vss value.
- `P_LATEST_EDGE_REFRESH`: Later rising or falling transitions refresh the corresponding captured trip value rather than leaving only the first measurement.
- `P_HYSTERESIS_WIDTH_SIGN`: After both directions are captured, hyst_width equals trip_rise minus trip_fall with that signed polarity.
- `P_VALID_AFTER_BOTH_DIRECTIONS`: Valid remains at vss until at least one rising and one falling trip have been captured, then rises to vdd.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `hysteresis_trip_characterizer.va`.
Every supplied `.va` file is editable; do not add or omit files.

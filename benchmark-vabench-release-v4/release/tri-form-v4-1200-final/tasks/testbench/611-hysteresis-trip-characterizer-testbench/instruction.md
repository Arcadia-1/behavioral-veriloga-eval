# Hysteresis Trip Characterizer Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Hysteresis Trip Characterizer` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_SUPPLY_MIDPOINT_THRESHOLD`: The characterizer detects cmp_out transitions through the instantaneous midpoint of vdd and vss.
- `P_RISING_TRIP_CAPTURE`: On each rising cmp_out midpoint crossing, trip_rise captures the instantaneous vin minus vss value.
- `P_FALLING_TRIP_CAPTURE`: On each falling cmp_out midpoint crossing, trip_fall captures the instantaneous vin minus vss value.
- `P_LATEST_EDGE_REFRESH`: Later rising or falling transitions refresh the corresponding captured trip value rather than leaving only the first measurement.
- `P_HYSTERESIS_WIDTH_SIGN`: After both directions are captured, hyst_width equals trip_rise minus trip_fall with that signed polarity.
- `P_VALID_AFTER_BOTH_DIRECTIONS`: Valid remains at vss until at least one rising and one falling trip have been captured, then rises to vdd.

The required trace names are: `time`, `vdd`, `vss`, `vin`, `cmp_out`, `trip_rise`, `trip_fall`, `hyst_width`, `valid`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.

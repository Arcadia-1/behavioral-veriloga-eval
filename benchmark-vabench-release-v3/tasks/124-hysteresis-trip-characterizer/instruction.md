# Hysteresis Trip Characterizer

Implement a voltage-domain measurement component that observes a comparator
input ramp and output decision waveform, captures the observable rising and
falling trip voltages, and reports the hysteresis width.

## Public Interface

Declare module `hysteresis_trip_characterizer` with positional ports `vdd, vss,
vin, cmp_out, trip_rise, trip_fall, hyst_width, valid`. All ports are
electrical. `vin` is the swept input being characterized, `cmp_out` is the
rail-coded comparator output, `trip_rise` and `trip_fall` are voltage-coded
captured trip points, `hyst_width` is the signed difference
`trip_rise - trip_fall`, and `valid` is a rail-coded flag that asserts after
both trip directions have been observed.

## Public Parameter Contract

Provide this overrideable public parameter:

- `tr = 20p`: output transition time for reported measurement voltages.

## Functional Contract

- Use the midpoint between `vdd` and `vss` as the decision threshold for
  `cmp_out`.
- When `cmp_out` rises through the midpoint, capture the instantaneous
  `vin - vss` value into `trip_rise`.
- When `cmp_out` falls through the midpoint, capture the instantaneous
  `vin - vss` value into `trip_fall`.
- Continue updating the captured values on later output transitions.
- Drive `hyst_width` as `trip_rise - trip_fall` once both captures are present.
- Drive `valid` low until both directions have been captured, then drive it
  high.

## Modeling Constraints

Return only `hysteresis_trip_characterizer.va`. Use deterministic
voltage-domain Verilog-A and voltage contributions only. The hysteretic
comparator under measurement is a supplied support artifact, not part of the
returned DUT. Do not modify or emit the support testbench, add checker logic,
hard-code waveform sample points, add simulator-private side channels, use
current contributions, `ddt()`, or `idt()`.

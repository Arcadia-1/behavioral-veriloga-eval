# Comparator Offset Search

Implement a voltage-domain measurement companion for a single-ramp comparator
offset search.

## Public Interface

Declare module `comparator_offset_search_ref` with positional ports `vdd, vss,
inp, inn, outp, trip_v, offset_est, valid`. All ports are electrical. `vdd` and
`vss` are supply rails, `inp` and `inn` are the differential comparator inputs,
`outp` is the voltage-coded comparator decision, and `trip_v`, `offset_est`,
and `valid` are measurement outputs.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vos = 5m V`: positive input-referred comparator offset.
- `trf = 20p`: transition smoothing time for decision and measurement outputs.

## Functional Contract

- Initialize `valid`, `trip_v`, and `offset_est` to a valid zero measurement
  state, and initialize `outp` consistently with the current differential input
  relative to `vos`.
- Drive `outp` high when `V(inp,vss) - V(inn,vss)` rises above `vos`.
- Drive `outp` low when the same differential input falls back below `vos`.
- On the first rising offset crossing, capture the input trip voltage on
  `trip_v`, capture the measured differential offset on `offset_est`, and
  assert `valid`.
- Keep the captured measurement stable after it becomes valid.
- Drive logic outputs rail-to-rail relative to `vdd` and `vss` using finite
  transition-style smoothing.

## Modeling Constraints

Return only `comparator_offset_search_ref.va`. Use voltage contributions only.
Do not modify or emit the support testbench, add checker logic, hard-code
waveform sample points, add simulator-private side channels, use
transistor-level devices, current contributions, AC/noise analysis, `ddt()`, or
`idt()`. Update retained decision and measurement state at crossing events and
drive voltage contributions outside those event blocks.

# Dynamic Supply Level Driver Audit

- Gate 1: `independent_l1_ready` as issue #109 numbered replacement row `499`. This
  row models a dynamic-supply electrical level driver whose input threshold and
  output levels are derived from the local `vdd`/`vss` rails, including local
  ground offset handling and under-supply fallback. It is not a fixed-threshold
  logic gate.
- Gate 2: `cadence_modeling_ready` for this replacement slice. Public
  prompt exposes the supply-referenced input threshold, rail-derived output
  fractions, under-supply low fallback, and transition timing without leaking
  checker sample windows. Fresh EVAS behavior validation passes visible and
  hidden gold and rejects all five negative variants on both splits. Fresh
  Spectre bridge validation passes visible and hidden gold and rejects all five
  hidden negative variants. EVAS lint preflight reports no diagnostics for
  visible or hidden solution decks. The solution keeps continuous rail
  expressions outside `transition()` and smooths the discrete output fraction.
  Spectre report triage found no task-level `AHDLLINT-*`, `VACOMP-1116`, or
  AHDL compile errors.
- Cadence reference correspondence: Cadence mixed-signal interface examples use
  dynamic local supplies and rail-referenced threshold/drive behavior. This
  row abstracts that connect-module pattern into a pure electrical DUT
  suitable for the voltage-domain vaBench surface.

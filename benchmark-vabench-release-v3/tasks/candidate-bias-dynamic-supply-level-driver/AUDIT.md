# Dynamic Supply Level Driver Audit

- Gate 1: `independent_l1_ready` as a non-numbered materialized replacement candidate. This
  row models a dynamic-supply electrical level driver whose input threshold and
  output levels are derived from the local `vdd`/`vss` rails, including local
  ground offset handling and under-supply fallback. It is not a fixed-threshold
  logic gate. It should not be counted as an appended benchmark row; if
  accepted, upstream should assign it to a replacement slot in the original
  `001`-`300` surface or keep it outside the scored denominator.
- Gate 2: `cadence_modeling_ready` for this replacement-candidate slice. Public
  prompt exposes the supply-referenced input threshold, rail-derived output
  fractions, under-supply low fallback, and transition timing without leaking
  checker sample windows. Targeted EVAS verification passes gold and rejects all
  five negative variants. Fresh Spectre bridge validation passes visible and
  hidden gold, and hidden Spectre negatives reject all five variants. EVAS lint
  preflight reports no diagnostics for visible or hidden solution decks. The
  solution keeps continuous rail expressions outside `transition()` and smooths
  the discrete output fraction, removing the initial `VACOMP-1116` warning seen
  during triage. AHDL log triage found no remaining task-level `AHDLLINT-*`,
  `VACOMP-1116`, or AHDL compile errors; only global bridge/Spectre setup
  notices such as `VACOMP-2435` and `SPECTRE-592` appear.
- Cadence reference correspondence: Cadence mixed-signal interface examples use
  dynamic local supplies and rail-referenced threshold/drive behavior. This
  candidate abstracts that connect-module pattern into a pure electrical DUT
  suitable for the voltage-domain vaBench surface.

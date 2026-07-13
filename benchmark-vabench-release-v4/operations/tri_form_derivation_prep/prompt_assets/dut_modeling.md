# Cadence Verilog-A Modeling Checklist

Declare modules, ports, disciplines, parameters, and structural instances
consistently across every source file. Place branch contributions in
continuously evaluated analog code; use event blocks to update stored state
rather than contain the contribution. Initialize analysis state when the model
requires a defined starting value.

Use `transition` for discrete or piecewise-constant values rather than direct
functions of continuously varying probes. Use `timer` for scheduled time events
instead of equality tests on `$abstime`. Preserve interface, parameter-override,
reset, hold, threshold, rail, and transition semantics when composing modules.

Before finalizing, check syntax, module dependencies, event directions, state
lifetime, and continuous contributions for portability and lint-clean behavior.

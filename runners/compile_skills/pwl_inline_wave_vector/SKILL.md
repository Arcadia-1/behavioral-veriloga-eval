# pwl_inline_wave_vector

## Trigger

Use this skill when EVAS/Spectre-strict reports `PWL wave must contain at least one time/value pair` for a generated Spectre `vsource type=pwl` stimulus.

## Rule

For this validator path, a PWL source must carry its time/value vector in an inline `wave=[t0 v0 t1 v1 ...]` attribute.  A bare source line followed by Spectre-style continuation rows can be parsed as a PWL source with no attached wave data.

## Repair Pattern

Convert continuation-style stimulus:

```spectre
Vin (in 0) vsource type=pwl
+ 0 0.0
+ 10n 0.6
+ 20n 0.2
```

into an inline wave vector:

```spectre
Vin (in 0) vsource type=pwl wave=[ 0 0.0 10n 0.6 20n 0.2 ]
```

If duplicate or non-increasing timestamps are present, compose with `pwl_monotonic_time` and nudge only the later timestamp by a femtosecond-scale epsilon.

## Safety Boundary

Only move already-generated public time/value pairs into the `wave=[...]` attribute.  Do not change node names, source names, voltage values, transient stop time, save statements, DUT instance order, or behavioral thresholds.  Accept the edit only through strict-EVAS/Spectre compile validation.

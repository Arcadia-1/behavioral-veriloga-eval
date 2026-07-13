# Cadence Verilog-A Repair Checklist

Inspect the complete module graph and distinguish parser, elaboration, lint,
and simulation failures from an incorrect behavioral relation. Trace the fault
through module interfaces and make the smallest semantic repair that addresses
the cause rather than one observed waveform point.

Preserve file structure, external interfaces, parameters, and unaffected
behavior. Recheck analog event directions, initialization and reset paths,
stored-state lifetime, continuous contributions, and `transition` usage before
finalizing the repaired bundle.

# Cadence Spectre Testbench Checklist

Use native Spectre netlist order: instance name, parenthesized node list,
master, then parameter assignments. Load Verilog-A models with `ahdl_include`.
Choose the voltage-source form that matches the intended stimulus: `type=dc`
with `dc`, `type=pulse` with `val0`, `val1`, timing parameters, `type=sine`
with `sinedc`, `ampl`, `freq`, or `type=pwl` with `wave=[time value ...]`.
Keep every PWL vector as complete time/value pairs and every continued
statement syntactically complete.

Declare a bounded transient analysis as `name tran stop=...`, adding `maxstep`
only when the intended event or waveform resolution requires it. Use `save` to
retain the input, control, output, and timing signals needed by the public
trace contract. Relate observations to the applied stimulus and distinguish a
behavioral mismatch from compilation failure, missing data, or an invalid run.

# Comparator Delay Overdrive Meter

Implement a voltage-domain measurement component that characterizes a clocked
comparator by measuring the delay from each clock decision edge to the resolved
decision output, while also reporting the input overdrive sampled at that clock
edge.

## Public Interface

Declare module `comparator_delay_overdrive_meter` with positional ports `vdd,
vss, clk, vinp, vinn, outp, outn, delay_ps, overdrive_mv, polarity, valid`. All
ports are electrical. `clk` is the comparator decision clock, `vinp`/`vinn` are
the differential comparator inputs, `outp`/`outn` are rail-coded decision
outputs from the comparator under measurement, `delay_ps` reports the measured
clock-to-decision delay in picoseconds, `overdrive_mv` reports
`abs(vinp - vinn)` in millivolts at the sampled clock edge, `polarity` is high
for an `outp` decision and low for an `outn` decision, and `valid` asserts after
a decision has been measured.

## Public Parameter Contract

Provide this overrideable public parameter:

- `tr = 20p`: output transition time for reported measurement voltages.

## Functional Contract

- Use the midpoint between `vdd` and `vss` as the clock and decision threshold.
- On each rising crossing of `clk`, store the current time and the absolute
  differential input overdrive.
- Arm exactly one pending measurement for the next decision output transition.
- When either `outp` or `outn` rises through the decision threshold while armed,
  report the elapsed time from the stored clock edge in picoseconds, report the
  stored overdrive in millivolts, set `polarity` according to which output
  resolved, assert `valid`, and disarm until the next clock edge.
- Hold the reported values between decisions.

## Modeling Constraints

Return only `comparator_delay_overdrive_meter.va`. Use deterministic
voltage-domain Verilog-A and voltage contributions only. The clocked comparator
under measurement is a supplied support artifact, not part of the returned DUT.
Do not modify or emit the support testbench, add checker logic, hard-code
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`.

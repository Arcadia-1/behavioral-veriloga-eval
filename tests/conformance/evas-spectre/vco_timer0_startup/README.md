# vco_timer0_startup

## Purpose

This conformance asset isolates the initial `timer(0,1n)` scheduling behavior
behind the historical `vbm1_vco_phase_integrator_bugfix` main120 row. It should
not be counted as a normal bugfix benchmark task.

## Semantic Axis

- Axis: `event-ordering`
- Expected EVAS/Spectre relation: `waveform_equivalent`
- Scope: `initial_step` initializes `ph=0`, then a coincident `timer(0,1n)`
  event updates phase before the first saved point.

## Gold Evidence

- `gold/vco_phase_integrator.va`
- `gold/tb_vco_phase_integrator_ref.scs`

At `t=0`, `vctrl=0.1 V`; the timer update is therefore
`0.03 + 0.09 * 0.1 = 0.039`. Spectre observes the settled initial phase near
`0.039 V` at the first saved point. EVAS should match that startup behavior and
should not emit an artificial initial transition from zero.

## Why This Is Not A Normal Bugfix Task

The observed risk is simulator startup ordering, not an LLM-repairable
functional defect in a supplied bad source. The VCO behavior can still be
promoted later as `spec-to-va` or `end-to-end` with post-startup metrics, but
the `timer(0)` startup rule belongs in EVAS/Spectre conformance.

## Runner Hook Needed

A conformance runner should:

1. run the included testbench on both EVAS and Spectre;
2. require both runs to compile and finish;
3. compare the initial saved `phase` value to the analytic `0.039 V` target;
4. require `clk` to remain low at startup;
5. compare early phase samples with a declared tolerance and report waveform
   drift separately from binary acceptance.

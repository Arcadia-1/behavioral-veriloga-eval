# vaBench Review Context

This context defines the language used when reviewing whether vaBench tasks are
admissible as independent benchmark coverage.

## Language

**Task Form**:
The artifact shape a task asks the solver to produce, such as a DUT, testbench,
bugfix, or end-to-end flow. A review does not change the task form unless the
task itself is rewritten.
_Avoid_: Task type

**Independent Function Credit**:
A counted benchmark credit for a task whose public prompt, gold solution,
checker, and negative variants validate a behaviorally distinct analog or
mixed-signal function.
_Avoid_: Count, slot

**Admission Status**:
The review decision for whether a task can enter the scored release surface,
remain as support or candidate evidence, or be removed/reworked before scoring.
_Avoid_: Task type, form

**Function Boundary Review**:
The first step of manual task review: decide whether the task represents a
behaviorally distinct analog or mixed-signal function worth preserving.
_Avoid_: Checker review

**Evaluation Alignment Review**:
The second step of manual task review: decide whether the current testbench,
checker, and negative variants actually measure the function boundary being
claimed.
_Avoid_: Function review

**Component Function Credit**:
A counted L1 credit for a local DUT whose behavior is useful as a reusable
analog or mixed-signal modeling component, even when it also appears inside an
L2 composed flow.
_Avoid_: Flow fragment

**Composed Flow Credit**:
A counted L2 credit for a task that evaluates integration across multiple
component functions or support artifacts, without replacing or duplicating the
component-function review.
_Avoid_: Duplicate component credit

**Circuit Source Function**:
A source, reference, oscillator, clock, supply, or stimulus-generator DUT that
models a reusable analog or mixed-signal circuit behavior rather than merely
supplying an external testbench waveform.
_Avoid_: Stimulus by default

**Testbench Stimulus**:
An external waveform or harness artifact whose role is to excite another DUT,
not to be evaluated as the circuit behavior under test.
_Avoid_: Source function

**L2 Support Component**:
A DUT-like helper module that is useful inside a composed L2 flow but is not
counted as an independent L1 circuit-function credit unless its prompt is
rewritten around a standalone circuit behavior.
_Avoid_: Independent L1 task

**Component-In-Flow Overlap**:
The acceptable relationship where an L2 composed flow reuses L1 component
functions that are also counted independently, provided the L1 tasks have
standalone function boundaries and the L2 task evaluates their integration.
_Avoid_: Duplicate task

**Core Circuit L2**:
A composed L2 task whose primary target is an analog or mixed-signal subsystem
behavior, such as a converter chain, PLL slice, calibration loop, receiver
front end, or power-management transient.
_Avoid_: Measurement flow

**Measurement L2**:
A composed L2 task whose primary target is building a reusable measurement,
characterization, or validation flow around circuit components rather than a
complete circuit subsystem.
_Avoid_: Core circuit L2

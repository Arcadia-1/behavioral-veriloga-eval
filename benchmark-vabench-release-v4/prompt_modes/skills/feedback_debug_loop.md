Feedback/debug skill:

Use this generic loop when an agentic run has access to the black-box feedback
oracle. The feedback output is debugging evidence, not a private-score oracle
and not a substitute for the public task contract.

1. First create the requested candidate `.va` file or files with the exact
   target names before running feedback.
2. Run the feedback command against the candidate source directory, then read
   the complete output before editing.
3. Triage failures in this order: AHDL-like preflight or lint diagnostics, EVAS
   compile errors, EVAS runtime errors, missing trace or signal availability,
   then behavior-property diagnostics.
4. For preflight or compile failures, repair syntax, includes, module names,
   port declarations, parameter declarations, unsupported constructs, and analog
   block structure before reasoning about behavior.
5. For missing or unusable traces, check exact public port names, exact target
   file names, continuous output contributions, and whether the model actually
   drives the public observable signals.
6. For behavior-property failures, map each diagnostic back to the public task
   contract. Use expected versus observed values, sample time, mismatch count,
   edge polarity, rail level, threshold, hold behavior, monotonicity, gain, or
   code-sequence clues to choose the next repair.
7. Change the model behavior, not the public interface. Do not add debug ports,
   pass/fail flags, file I/O side channels, or extra observables to satisfy a
   feedback run.
8. You may inspect the public feedback testbench when it is mounted, but do not
   hard-code one stimulus, one time grid, one sample window, or one apparent
   corner. Generalize from the public contract and use feedback only to locate
   mistakes.
9. After every meaningful edit, rerun the feedback command and compare the new
   failure mode with the previous one.
10. If feedback passes, still do a final consistency check against the public
    task contract, target artifact names, parameters, and modeling constraints.
11. Never request or rely on private score testbenches, evaluator-only checker
    profiles, private checker internals, reference solutions, or negative
    variants.

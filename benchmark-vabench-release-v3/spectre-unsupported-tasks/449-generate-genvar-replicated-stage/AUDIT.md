# Archived Audit: Generate Genvar Replicated Stage

- Task: `449-generate-genvar-replicated-stage`
- Status: archived Spectre-unsupported candidate; not counted in the active default v3 denominator.
- Removal reason: generate/genvar with AMS digital/wreal constructs outside the default standalone Spectre Verilog-A target.
- Gate 1: not an ordinary standalone Spectre-compatible circuit-function benchmark in the current v3 surface.
- Gate 2: public instruction has been normalized to the current vaBench section format. Starter, solution, tests, and negative variants are unchanged in this cleanup.
- Verification status: no fresh Spectre or AHDL rerun was performed for this cleanup because the row remains archived and unsupported by the current default Spectre target.
- Future action: Potential future rescue only if rebuilt as a real repeated electrical stage; the current one-stage wreal pass-through is too weak.

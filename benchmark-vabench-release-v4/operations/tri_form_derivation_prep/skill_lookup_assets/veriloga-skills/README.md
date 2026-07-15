# veriloga-skills

Instructs an Agent to write Verilog-A behavioral models that conform to Cadence Virtuoso conventions and can be used directly inside Virtuoso.

## vaBench vendored snapshot

This copy is a **read-only, release-pinned subset** used by vaBench skill lookup
modes. Do not clone GitHub or install a different copy during an experiment.
Use only the files present in this directory so the run can be reproduced from
the benchmark manifest and snapshot hash.

Included in this vaBench subset:

- `veriloga/SKILL.md`
- `veriloga/references/`
- `veriloga/assets/template.va`
- `evas-sim/SKILL.md`

Not included in this subset: `openvaf/`, runnable example trees, tests, and
GitHub workflow files. If a referenced example path is absent, use the local
template and reference notes instead of attempting remote retrieval.

> **If you are a human**: the skill overview and structure below will help you understand what this package contains. After installation, ask the Agent to write Verilog-A for you.

> **If you are an AI Agent in vaBench skill lookup mode**: do not install
> anything. Read local files only. Start with `veriloga/SKILL.md` for DUT
> authoring rules. For a `.scs` testbench submission, read
> `veriloga/references/spectre-testbench-submission-checklist.md` and the
> public task binding before writing the final answer.

---

## Skill Overview

| Skill | Role | Function |
|-------|------|----------|
| **veriloga** | Core — code writing | Mandatory Verilog-A rules, circuit-category references, and Spectre testbench notes; produces Verilog-A ready to drop into a Virtuoso cellview |
| **evas-sim** | Optional — voltage-domain verification reference | Describes EVAS-compatible Spectre netlists and portability pitfalls |
| **openvaf** | Not included in this vaBench subset | Use only if installed outside this release for a separate current-domain flow |

`veriloga` is the core skill and handles all code writing on its own. `evas-sim` and `openvaf` are optional companion skills for local verification of voltage-domain and current-domain modules respectively.

---

## Skill 1: veriloga

Rules and patterns distilled from 1,809 real `.va` designs, covering 12 circuit categories for analog/mixed-signal IC design. Generated code conforms to Cadence Virtuoso / Spectre conventions and can be placed directly into a cellview.

Contains mandatory Verilog-A rules, circuit-category references, and a compact
Spectre testbench submission checklist. See [`veriloga/SKILL.md`](./veriloga/SKILL.md).

---

## Local Verification (Optional)

Finished modules can be verified locally. There are two verification paths depending on the constructs used in the code:

| Method | Applicable modules | Deciding criterion | Tool |
|--------|-------------------|--------------------|------|
| **EVAS** | Voltage-domain | `V() <+` + `@(cross())` / `transition()`, no `I() <+` | [EVAS](https://evas.tokenzhang.com/) event-driven simulator |
| **OpenVAF + ngspice** | Current-domain | `I() <+` / `ddt()` / `idt()` / `laplace_nd()` | `openvaf` skill |

```
Finish module → scan analog begin → classify domain
                                    ├── voltage-domain → EVAS verification
                                    ├── current-domain → OpenVAF compile + ngspice simulation
                                    └── mixed-domain   → recommended: split into two sub-modules
```

- **Voltage-domain** typical modules: SAR logic, DFF, counter, comparator, data generator
- **Current-domain** typical modules: Opamp, RLC network, VCO core, LDO, filter

Full domain classification and routing logic: `veriloga/references/domain-routing.md`.

### Skill 2: evas-sim

Handles simulation verification for voltage-domain modules:

```
.va file → EVAS event-driven simulation → waveform verification
```

Covers: EVAS installation and configuration, simulation commands, waveform viewing, list of supported constructs, troubleshooting guide. See [`evas-sim/SKILL.md`](./evas-sim/SKILL.md).

### Skill 3: openvaf

Handles compilation and simulation for current-domain modules:

```
.va file → OpenVAF compile → .osdi file → ngspice load → simulation verification
```

Covers: OpenVAF installation and configuration, compile commands, ngspice OSDI loading, list of supported features, troubleshooting guide.

This vaBench snapshot does not include `openvaf/`; do not rely on it during a
benchmark skill lookup run unless the experiment explicitly mounts that skill
as a separate, version-pinned resource.

---

## Installation

> For normal use outside vaBench, install from GitHub as described below. For
> vaBench experiments, skip installation and use the vendored files already
> present in the release.

**Step 1 — Choose installation scope**

| Scenario | Choice |
|----------|--------|
| Current project only (default, recommended) | Project-level install → `.agent/skills/` |
| All projects | Global install → `~/.agent/skills/` |

> Outside vaBench, use project-level installation by default. Replace `.agent/skills/` with your agent's skill directory if it uses a different path. Inside vaBench, do not run these installation commands during an experiment.

**Step 2 — Run the install command** (bash; works on macOS / Linux / Windows)

Project-level (default; run from the project root):
```bash
git clone --depth 1 https://github.com/Arcadia-1/veriloga-skills /tmp/veriloga-skills \
  && mkdir -p .agent/skills \
  && cp -r /tmp/veriloga-skills/{veriloga,evas-sim,openvaf} .agent/skills/ \
  && rm -rf /tmp/veriloga-skills
```

Global (optional):
```bash
git clone --depth 1 https://github.com/Arcadia-1/veriloga-skills /tmp/veriloga-skills \
  && mkdir -p ~/.agent/skills \
  && cp -r /tmp/veriloga-skills/{veriloga,evas-sim,openvaf} ~/.agent/skills/ \
  && rm -rf /tmp/veriloga-skills
```

**Step 3 — Verify**

Run `/skills` in the Agent; confirm `veriloga`, `evas-sim`, and `openvaf` appear in the output list ✅

> **If you are an AI Agent outside vaBench**: execute the project-level installation by default. Use the global path only if the user explicitly wants a home-directory install. After installation, read `veriloga/SKILL.md` and start working. In vaBench skill lookup mode, the local snapshot is already mounted; read it directly.

### Project Customization

Edit `veriloga/references/customize.md` to override defaults: port naming conventions, supply voltages, file-header templates, simulator-specific options, etc.

## Requirements

- **veriloga skill**: no external dependencies — pure documentation/reference skill
- **Local verification (optional)**:
  - Voltage-domain → [EVAS](https://evas.tokenzhang.com/)
  - Current-domain → [OpenVAF](https://openvaf.semimod.de/) + [ngspice](http://ngspice.sourceforge.net/) (≥ 38, with OSDI support)

See [requirements.md](./requirements.md) for details.

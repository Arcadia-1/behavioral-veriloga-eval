# EVAS Speed Server Feasibility 2026-05-21

## Result

Server-side EVAS speed experiments are feasible in principle, but the current
`thu-wei` default shell is not ready to run this EVAS Python workflow.

## Evidence

- Virtuoso bridge profile `ci` reaches the running CIW daemon on `thu-wei`.
- The same profile reports `VB_REMOTE_HOST_ci must be set` for the Spectre
  runner path, so the current bridge profile is not a complete same-slice
  EVAS/Spectre timing environment.
- SSH to `thu-wei` succeeds through `thu-sui` and `thu-han`.
- SSH through `thu-jin` times out during banner exchange.
- The default `thu-wei` environment reports `python3: Command not found`.
- The default `thu-wei` environment has `/usr/bin/python` as Python 2.7.5.
- No default `evas` executable was found in the probed shell environment.

## Blocker

The blocker is runtime provisioning: configure a Python 3 environment and
install EVAS on `thu-wei`, or run the experiment through a container/module
that provides Python 3 plus the EVAS package. After that, the local P0-P3
runner can be copied to the server and rerun on the same release rows.

## Safe Next Command Shape

Use `thu-sui` or `thu-han` as the jump host for deployment probes. Avoid relying
on the current `thu-jin` path until the banner timeout is resolved.

## `thu-sui` Same-Server Option

`thu-sui` is a better EVAS host than `thu-wei`: it has Python 3.9.21, pip, and
`venv` support in the default environment. EVAS can likely be deployed there in
a user-local virtual environment.

Running `setup_tsmc180` inside `~/TSMC180` succeeds and creates the expected PDK
working-directory files:

- `.cdsinit`, `.cdsenv`, `display.drf`, and `blindkey.skl` symlink to
  `/home/dmanager/shared_lib/TSMC180MS/`.
- `cds.lib`, `cdsLibMgr.il`, `extra.lib`, `calibre/`, `dummy/`, and `manual`
  are created/copied.
- The setup script is
  `/home/dmanager/shared_lib/TSMC180MS/setup_tsmc180`.

This confirms TSMC180 PDK directory initialization, but it does not initialize
the command-line Cadence/Spectre executable environment.

Current probe does not show Spectre/Cadence on `thu-sui`:

- `spectre` and `virtuoso` are not on the default `PATH`.
- `source ~/.cshrc` does not expose `spectre` or `virtuoso`.
- Environment modules are available, but only the default modulefiles are listed.
- A bounded search under `/edamgr`, `/server_local`, `/server_local_ssd`, and
  `/ramic` did not find a `spectre` executable.

The missing executable setup path was later identified:

```csh
source /home/cshrc/.cshrc.cadence.sui
```

After sourcing it from `~/TSMC180`, `spectre` resolves to
`/edamgr/Spectre/SPECTRE211Hotfix/tools/bin/spectre`, `virtuoso` resolves to
`/edamgr/Virtuoso/IC618Hotfix4/tools/dfII/bin/virtuoso`, and `spectre -W`
reports `21.1.0.509.isr12`.

A convenience script has been installed on `thu-sui`:

```csh
cd ~/TSMC180
source ./setup_cadence_sui.csh
```

This makes `thu-sui` a viable candidate for same-server EVAS/Spectre timing,
pending EVAS virtualenv installation and a small same-row smoke run.

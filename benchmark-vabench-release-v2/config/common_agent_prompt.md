# Common vaBench v2 Agent Rules

This is a one-shot behavioral Verilog-A benchmark task. Follow the public task
specification and return only the requested target artifact contents.

Public interface rules:

- Target artifact filenames are exact; do not rename, omit, or add files.
- Module, subcircuit, port, and top-level net names required by the task or
  support files are exact public interface names.
- Saved signal names are part of the public contract. Each saved waveform name
  must be
  an actual top-level Spectre net connected to the relevant source, DUT port,
  interconnect, or monitor output; do not route behavior through alias nets and
  then save unconnected public names.
- If a Spectre PWL `wave=[...]` array spans multiple physical lines, use legal
  Spectre line continuation or keep the array on one physical line.
- Treat supplied support files as read-only inputs. Do not return support files
  unless they are also listed as target artifacts.
- Do not mention or depend on private checker code, gold implementations, hidden
  thresholds, or non-public file paths.

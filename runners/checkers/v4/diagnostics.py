"""Property-level diagnostics for task-specific v4 checkers."""
from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Union

from ..api import Checker


_FIELD_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)=([^\s;]+)")
MetricSpec = Union[str, Sequence[str]]
DIAGNOSTIC_SCHEMA = "v4-checker-diagnostic-v1"


def excess_count(observed: int, allowed: int = 0) -> int:
    """Return the number of mismatches beyond an accepted sampling allowance."""

    return max(0, int(observed) - int(allowed))


def _fields(note: str) -> dict[str, str]:
    return {key: value.rstrip(",") for key, value in _FIELD_RE.findall(note)}


def _metric_count(fields: Mapping[str, str], spec: str) -> int:
    inverted = spec.startswith("!")
    key = spec[1:] if inverted else spec
    raw = fields.get(key)
    if raw is None:
        return 0
    if inverted:
        return 0 if raw.lower() in {"true", "1", "yes"} else 1
    try:
        value = float(raw)
    except ValueError:
        return 0
    return max(0, int(round(abs(value))))


def with_property_diagnostics(
    checker: Checker,
    property_metrics: Mapping[str, MetricSpec],
) -> Checker:
    """Append property mismatch counts using task-local metric declarations."""

    def wrapped(rows: list[dict[str, float]]) -> tuple[bool, str]:
        ok, note = checker(rows)
        fields = _fields(note)
        diagnostics: list[str] = []
        for property_id, raw_specs in property_metrics.items():
            specs = (raw_specs,) if isinstance(raw_specs, str) else tuple(raw_specs)
            mismatch_count = sum(_metric_count(fields, spec) for spec in specs)
            diagnostics.append(f"{property_id} mismatch_count={mismatch_count}")
        note = note + "; " + "; ".join(diagnostics)
        return ok, _append_contract(note, ok)

    wrapped.__name__ = checker.__name__
    wrapped.__doc__ = checker.__doc__
    wrapped.__module__ = checker.__module__
    return wrapped


def _append_contract(note: str, ok: bool) -> str:
    """Expose a redacted, machine-readable result envelope for feedback."""
    status = "pass" if ok else "fail"
    category = "behavior_pass" if ok else "behavior_mismatch"
    return (
        f"{note}; diagnostic_schema={DIAGNOSTIC_SCHEMA} status={status} "
        f"category={category} event=stimulus_relative event_context=stimulus_relative "
        "expected=public_contract observed=trace"
    )


def with_diagnostic_contract(checker: Checker) -> Checker:
    """Add the common diagnostic envelope without changing checker semantics."""

    def wrapped(rows: list[dict[str, float]]) -> tuple[bool, str]:
        ok, note = checker(rows)
        return ok, _append_contract(note, ok)

    wrapped.__name__ = checker.__name__
    wrapped.__doc__ = checker.__doc__
    wrapped.__module__ = checker.__module__
    return wrapped

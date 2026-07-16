"""Diagnostic binding scoped to repaired V4 families 271-280."""
from __future__ import annotations

from collections.abc import Iterable

from ..api import Checker, Row
from .stimulus_relative import structured_result


def bind_properties(checker: Checker, property_ids: Iterable[str]) -> Checker:
    property_tuple = tuple(property_ids)
    structured = structured_result(checker, property_tuple)

    def wrapped(rows: list[Row]) -> tuple[bool, str]:
        passed, note = structured(rows)
        return passed, f"{note}; checked_property_ids={','.join(property_tuple)}"

    wrapped.__name__ = checker.__name__
    wrapped.__doc__ = checker.__doc__
    wrapped.__module__ = checker.__module__
    return wrapped

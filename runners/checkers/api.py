"""Shared type contract for row-based behavior checkers."""

from __future__ import annotations

from collections.abc import Callable


Row = dict[str, float]
CheckResult = tuple[bool, str]
Checker = Callable[[list[Row]], CheckResult]


"""Task-specific vaBench behavior checkers."""

from __future__ import annotations

import sys


# Candidate modules imported from the v4 pilot used the package name
# ``checkers`` directly.  Current repository-root imports use
# ``runners.checkers``.  Keep both import paths pointing at the same package so
# mechanically migrated checkers remain loadable without rewriting 400 files.
sys.modules.setdefault("checkers", sys.modules[__name__])

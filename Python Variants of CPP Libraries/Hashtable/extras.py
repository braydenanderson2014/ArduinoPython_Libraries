"""Compatibility bundle for all optional hashtable helpers.

Import the specific modules instead when you only need one feature area:
- iterating.py
- sorting.py
- stats.py
"""

from __future__ import annotations

from typing import Any

try:
	from .iterating import IteratingHashtableMixin
	from .sorting import SortingHashtableMixin
	from .stats import StatsHashtableMixin
	from .core import ArduinoHashTable
except ImportError:
	from iterating import IteratingHashtableMixin  # type: ignore[no-redef]
	from sorting import SortingHashtableMixin  # type: ignore[no-redef]
	from stats import StatsHashtableMixin  # type: ignore[no-redef]
	from core import ArduinoHashTable  # type: ignore[no-redef]


class ArduinoHashTableExtras(
	IteratingHashtableMixin,
	SortingHashtableMixin,
	StatsHashtableMixin,
	ArduinoHashTable,
):
	"""Core hashtable plus all optional helper areas."""


ArduinoHashTableFull = ArduinoHashTableExtras

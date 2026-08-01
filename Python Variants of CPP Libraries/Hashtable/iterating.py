"""Iterating helpers for ArduinoHashTable.

Import this module when you only need iteration-oriented helpers.
"""

from __future__ import annotations

from typing import Any, Iterable, Tuple

try:
	from .core import ArduinoHashTable
except ImportError:
	from core import ArduinoHashTable  # type: ignore[no-redef]


class IteratingHashtableMixin:
	"""Adds keys, values, and items iteration helpers."""

	def keys(self) -> Iterable[Any]:
		for bucket in self._buckets:
			for key, _ in bucket:
				yield key

	def values(self) -> Iterable[Any]:
		for bucket in self._buckets:
			for _, value in bucket:
				yield value

	def items(self) -> Iterable[Tuple[Any, Any]]:
		for bucket in self._buckets:
			for key, value in bucket:
				yield key, value


class IteratingHashtable(IteratingHashtableMixin, ArduinoHashTable):
	"""Core hashtable with iteration helpers."""

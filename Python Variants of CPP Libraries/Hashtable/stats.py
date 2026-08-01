"""Stats helpers for ArduinoHashTable.

Import this module when you only need table inspection helpers.
"""

from __future__ import annotations

from typing import Any, Dict

try:
	from .core import ArduinoHashTable
except ImportError:
	from core import ArduinoHashTable  # type: ignore[no-redef]


class StatsHashtableMixin:
	"""Adds lightweight inspection helpers."""

	def stats(self) -> Dict[str, Any]:
		chain_lengths = [len(b) for b in self._buckets]
		max_chain = max(chain_lengths) if chain_lengths else 0
		return {
			"mode": self.mode.value,
			"size": self.size,
			"capacity": self.capacity,
			"load": self.load,
			"max_chain": max_chain,
			"max_entries": self._max_entries,
		}

	def __len__(self) -> int:
		return self.size

	def __contains__(self, key: Any) -> bool:
		return self.contains(key)

	def __setitem__(self, key: Any, value: Any) -> None:
		self.put(key, value)

	def __getitem__(self, key: Any) -> Any:
		value = self.get(key, default=None)
		if value is None and not self.contains(key):
			raise KeyError(key)
		return value

	def __delitem__(self, key: Any) -> None:
		if not self.remove(key):
			raise KeyError(key)

	def __repr__(self) -> str:
		return (
			f"{self.__class__.__name__}(mode={self.mode.value!r}, size={self.size}, "
			f"capacity={self.capacity})"
		)


class StatsHashtable(StatsHashtableMixin, ArduinoHashTable):
	"""Core hashtable with inspection helpers."""

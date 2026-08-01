"""Sorting helpers for ArduinoHashTable.

Import this module when you only need sorted views of the table.
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional, Tuple

try:
	from .core import ArduinoHashTable
except ImportError:
	from core import ArduinoHashTable  # type: ignore[no-redef]


class SortingHashtableMixin:
	"""Adds sorted key, value, and item views."""

	def _collect_items(self) -> List[Tuple[Any, Any]]:
		items: List[Tuple[Any, Any]] = []
		for bucket in self._buckets:
			for key, value in bucket:
				items.append((key, value))
		return items

	def sorted_keys(
		self,
		reverse: bool = False,
		key: Optional[Callable[[Any], Any]] = None,
	) -> List[Any]:
		keys: List[Any] = []
		for item_key, _ in self._collect_items():
			keys.append(item_key)
		return sorted(keys, key=key, reverse=reverse)

	def sorted_values(
		self,
		reverse: bool = False,
		key: Optional[Callable[[Any], Any]] = None,
	) -> List[Any]:
		values: List[Any] = []
		for _, item_value in self._collect_items():
			values.append(item_value)
		return sorted(values, key=key, reverse=reverse)

	def sorted_items(
		self,
		reverse: bool = False,
		key: Optional[Callable[[Tuple[Any, Any]], Any]] = None,
	) -> List[Tuple[Any, Any]]:
		return sorted(self._collect_items(), key=key, reverse=reverse)


class SortingHashtable(SortingHashtableMixin, ArduinoHashTable):
	"""Core hashtable with sorted-view helpers."""

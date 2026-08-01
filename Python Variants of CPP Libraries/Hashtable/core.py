"""Hashtable core with switchable fixed and dynamic modes.

This module is designed to mirror embedded constraints while still being
easy to test in Python.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional, Tuple


try:
	from Optional.optional_value import OptionalValue
except Exception:
	class OptionalValue:
		"""Fallback Optional wrapper if shared module import is unavailable."""

		def __init__(self, value: Any = None, has_value: bool = False) -> None:
			self._value = value
			self._has_value = has_value

		@staticmethod
		def of(value: Any) -> "OptionalValue":
			return OptionalValue(value=value, has_value=True)

		@staticmethod
		def empty() -> "OptionalValue":
			return OptionalValue()

		def has_value(self) -> bool:
			return self._has_value

		def is_present(self) -> bool:
			return self._has_value

		def get_value(self) -> Any:
			if not self._has_value:
				raise ValueError("OptionalValue is empty")
			return self._value

		def or_else(self, default_value: Any) -> Any:
			return self._value if self._has_value else default_value

		def if_present(self, fn: Any) -> None:
			if self._has_value:
				fn(self._value)

		def hasValue(self) -> bool:
			return self.has_value()

		def isPresent(self) -> bool:
			return self.is_present()

		def getValue(self) -> Any:
			return self.get_value()

		def orElse(self, default_value: Any) -> Any:
			return self.or_else(default_value)

		def ifPresent(self, fn: Any) -> None:
			self.if_present(fn)

		def __bool__(self) -> bool:
			return self._has_value

		def __repr__(self) -> str:
			if self._has_value:
				return f"OptionalValue({self._value!r})"
			return "OptionalValue.empty()"


class TableMode(str, Enum):
	FIXED = "fixed"
	DYNAMIC = "dynamic"


class ArduinoHashTable:
	"""A chained-bucket hashtable with mode switching.

	Modes:
	- fixed: bucket count never grows automatically
	- dynamic: bucket count grows when load factor threshold is exceeded
	"""

	def __init__(
		self,
		capacity: int = 16,
		mode: str = TableMode.DYNAMIC,
		load_factor: float = 0.70,
		growth_factor: int = 2,
		max_entries: Optional[int] = None,
	) -> None:
		if capacity <= 0:
			raise ValueError("capacity must be > 0")
		if not 0 < load_factor <= 1:
			raise ValueError("load_factor must be in (0, 1]")
		if growth_factor < 2:
			raise ValueError("growth_factor must be >= 2")

		self._mode = self._normalize_mode(mode)
		self._load_factor = load_factor
		self._growth_factor = growth_factor
		self._max_entries = max_entries

		self._buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(capacity)]
		self._size = 0

		if self._mode == TableMode.FIXED and max_entries is not None and max_entries < 0:
			raise ValueError("max_entries must be >= 0 or None")

	@staticmethod
	def _normalize_mode(mode: str) -> TableMode:
		try:
			return TableMode(mode)
		except ValueError as exc:
			raise ValueError("mode must be 'fixed' or 'dynamic'") from exc

	@property
	def mode(self) -> TableMode:
		return self._mode

	@property
	def capacity(self) -> int:
		return len(self._buckets)

	@property
	def size(self) -> int:
		return self._size

	@property
	def load(self) -> float:
		return self._size / max(1, self.capacity)

	def set_mode(self, mode: str, max_entries: Optional[int] = None) -> None:
		"""Switch table mode without rebuilding object state."""
		normalized = self._normalize_mode(mode)
		if normalized == TableMode.FIXED:
			if max_entries is not None and max_entries < 0:
				raise ValueError("max_entries must be >= 0 or None")
			if max_entries is not None and self._size > max_entries:
				raise ValueError("current size exceeds max_entries")
			if max_entries is not None:
				self._max_entries = max_entries
		else:
			self._max_entries = None

		self._mode = normalized

	def use_fixed_mode(self, max_entries: Optional[int] = None) -> None:
		self.set_mode(TableMode.FIXED, max_entries=max_entries)

	def use_dynamic_mode(self) -> None:
		self.set_mode(TableMode.DYNAMIC)

	def _stable_hash(self, key: Any) -> int:
		"""Deterministic hash for repeatable behavior across Python runs."""
		if isinstance(key, int):
			return key & 0x7FFFFFFF

		if isinstance(key, bytes):
			data = key
		elif isinstance(key, str):
			data = key.encode("utf-8", "replace")
		else:
			data = str(key).encode("utf-8", "replace")

		h = 2166136261
		for b in data:
			h ^= b
			h = (h * 16777619) & 0xFFFFFFFF
		return h

	def _index(self, key: Any) -> int:
		return self._stable_hash(key) % self.capacity

	def _find_in_bucket(self, bucket: List[Tuple[Any, Any]], key: Any) -> int:
		for i, (k, _) in enumerate(bucket):
			if k == key:
				return i
		return -1

	def _ensure_growth(self) -> None:
		if self._mode != TableMode.DYNAMIC:
			return
		if self.load <= self._load_factor:
			return
		self.resize(max(1, self.capacity * self._growth_factor))

	def resize(self, new_capacity: int) -> None:
		"""Rebuild buckets at a new capacity.

		This is always allowed as an explicit operation. Automatic growth
		only occurs in dynamic mode.
		"""
		if new_capacity <= 0:
			raise ValueError("new_capacity must be > 0")

		old_items = []
		for bucket in self._buckets:
			for key, value in bucket:
				old_items.append((key, value))

		self._buckets = [[] for _ in range(new_capacity)]
		self._size = 0

		for k, v in old_items:
			self.put(k, v)

	def put(self, key: Any, value: Any) -> None:
		if self._mode == TableMode.FIXED and self._max_entries is not None and self._size >= self._max_entries:
			# Updates are still allowed when key already exists.
			idx = self._index(key)
			bucket = self._buckets[idx]
			if self._find_in_bucket(bucket, key) < 0:
				raise OverflowError("fixed table entry limit reached")

		idx = self._index(key)
		bucket = self._buckets[idx]
		hit = self._find_in_bucket(bucket, key)

		if hit >= 0:
			bucket[hit] = (key, value)
			return

		bucket.append((key, value))
		self._size += 1
		self._ensure_growth()

	def get(self, key: Any, default: Any = None, as_optional: bool = False) -> Any:
		"""Get value by key.

		- default behavior: return value or default
		- as_optional=True: return OptionalValue
		"""
		if as_optional:
			return self.get_optional(key)

		idx = self._index(key)
		bucket = self._buckets[idx]
		hit = self._find_in_bucket(bucket, key)
		if hit >= 0:
			return bucket[hit][1]
		return default

	def get_optional(self, key: Any) -> OptionalValue:
		idx = self._index(key)
		bucket = self._buckets[idx]
		hit = self._find_in_bucket(bucket, key)
		if hit >= 0:
			return OptionalValue.of(bucket[hit][1])
		return OptionalValue.empty()

	def remove(self, key: Any) -> bool:
		idx = self._index(key)
		bucket = self._buckets[idx]
		hit = self._find_in_bucket(bucket, key)
		if hit < 0:
			return False

		bucket.pop(hit)
		self._size -= 1
		return True

	def contains(self, key: Any) -> bool:
		idx = self._index(key)
		return self._find_in_bucket(self._buckets[idx], key) >= 0

	def clear(self) -> None:
		self._buckets = [[] for _ in range(self.capacity)]
		self._size = 0


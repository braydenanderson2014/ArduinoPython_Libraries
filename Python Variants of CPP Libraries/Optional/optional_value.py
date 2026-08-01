"""Optional value wrapper for Python and MicroPython.

MicroPython does not provide a runtime optional container like C++ Optional<T>.
This module provides a small compatible wrapper.
"""

from __future__ import annotations

try:
	from typing import Any, Callable
except ImportError:
	Any = object  # type: ignore[assignment]
	Callable = object  # type: ignore[assignment]


class OptionalValue:
	"""Small Optional wrapper that mirrors Arduino Optional<T> style."""

	__slots__ = ("_value", "_has_value")

	def __init__(self, value: Any = None, has_value: bool = False) -> None:
		self._value = value
		self._has_value = has_value

	@staticmethod
	def of(value: Any) -> "OptionalValue":
		return OptionalValue(value=value, has_value=True)

	@staticmethod
	def empty() -> "OptionalValue":
		return OptionalValue()

	@staticmethod
	def of_nullable(value: Any) -> "OptionalValue":
		if value is None:
			return OptionalValue.empty()
		return OptionalValue.of(value)

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

	def if_present(self, fn: Callable[[Any], None]) -> None:
		if self._has_value:
			fn(self._value)

	# C++-style aliases for consistency with the Arduino Optional API.
	def hasValue(self) -> bool:
		return self.has_value()

	def isPresent(self) -> bool:
		return self.is_present()

	def getValue(self) -> Any:
		return self.get_value()

	def orElse(self, default_value: Any) -> Any:
		return self.or_else(default_value)

	def ifPresent(self, fn: Callable[[Any], None]) -> None:
		self.if_present(fn)

	def __bool__(self) -> bool:
		return self._has_value

	def __repr__(self) -> str:
		if self._has_value:
			return f"OptionalValue({self._value!r})"
		return "OptionalValue.empty()"

"""Core properties storage for Arduino-style Python projects.

This module keeps the memory footprint small and only provides the base
key/value store plus generic .properties-style text handling.
Format-specific helpers live in Properties/formats/.
"""

from __future__ import annotations

try:
	from Hashtable.core import ArduinoHashTable
except Exception:
	raise ImportError(
		"Properties.core requires the sibling Hashtable package to be importable"
	)

try:
	from Optional.optional_value import OptionalValue
except Exception:
	class OptionalValue:
		__slots__ = ("_value", "_has_value")

		def __init__(self, value=None, has_value=False):
			self._value = value
			self._has_value = has_value

		@staticmethod
		def of(value):
			return OptionalValue(value=value, has_value=True)

		@staticmethod
		def empty():
			return OptionalValue()

		def has_value(self):
			return self._has_value

		def is_present(self):
			return self._has_value

		def get_value(self):
			if not self._has_value:
				raise ValueError("OptionalValue is empty")
			return self._value

		def or_else(self, default_value):
			return self._value if self._has_value else default_value

		def if_present(self, fn):
			if self._has_value:
				fn(self._value)

		def hasValue(self):
			return self.has_value()

		def isPresent(self):
			return self.is_present()

		def getValue(self):
			return self.get_value()

		def orElse(self, default_value):
			return self.or_else(default_value)

		def ifPresent(self, fn):
			self.if_present(fn)

		def __bool__(self):
			return self._has_value

		def __repr__(self):
			if self._has_value:
				return "OptionalValue(%r)" % (self._value,)
			return "OptionalValue.empty()"


DEFAULT_FILE_TYPES = (".properties",)
DEFAULT_COMMENT_PREFIXES = ("#", ";")
DEFAULT_SEPARATOR = "="


class Properties:
	"""Small key/value store backed by ArduinoHashTable."""

	__slots__ = ("_table", "_separator", "_comment_prefixes")

	def __init__(self, capacity=16, mode="dynamic", separator=DEFAULT_SEPARATOR, comment_prefixes=DEFAULT_COMMENT_PREFIXES):
		self._table = ArduinoHashTable(capacity=capacity, mode=mode)
		self._separator = separator
		self._comment_prefixes = tuple(comment_prefixes)

	@classmethod
	def supported_file_types(cls):
		return DEFAULT_FILE_TYPES

	@property
	def table(self):
		return self._table

	def set_property(self, key, value):
		self._table.put(str(key), "" if value is None else str(value))

	def get_property(self, key, default_value=None):
		if self.contains_key(key):
			return self._table.get(key, default_value)
		return default_value

	def get_optional(self, key):
		if self.contains_key(key):
			return OptionalValue.of(self._table.get(key))
		return OptionalValue.empty()

	def remove_property(self, key):
		return self._table.remove(key)

	def contains_key(self, key):
		return self._table.contains(key)

	def exists(self, key, value=None):
		if not self.contains_key(key):
			return False
		if value is None:
			return True
		return self.get_property(key) == str(value)

	def clear(self):
		self._table.clear()

	def size(self):
		return self._table.capacity

	def elements(self):
		return self._table.size

	def is_empty(self):
		return self._table.size == 0

	def iter_items(self):
		for bucket in self._table._buckets:
			for key, value in bucket:
				yield key, value

	def iter_keys(self):
		for key, _ in self.iter_items():
			yield key

	def iter_values(self):
		for _, value in self.iter_items():
			yield value

	def to_dict(self):
		mapping = {}
		for key, value in self.iter_items():
			mapping[key] = value
		return mapping

	def from_dict(self, mapping, clear_first=True):
		if clear_first:
			self.clear()
		for key in mapping:
			self.set_property(key, mapping[key])

	def _split_line(self, line, separators=None):
		if separators is None:
			separators = (self._separator, ":", "=")
		for separator in separators:
			index = line.find(separator)
			if index > 0:
				return line[:index].strip(), line[index + len(separator):].strip()
		return None, None

	def load_text(self, text, separators=None, clear_first=True):
		if clear_first:
			self.clear()

		count = 0
		for raw_line in text.splitlines():
			line = raw_line.strip()
			if not line:
				continue
			if line[0] in self._comment_prefixes:
				continue
			key, value = self._split_line(line, separators=separators)
			if key is None:
				continue
			self.set_property(key, value)
			count += 1
		return count

	def save_text(self, comments=None, separator=None):
		if separator is None:
			separator = self._separator

		lines = []
		if comments:
			for comment_line in str(comments).splitlines():
				lines.append("# " + comment_line if comment_line else "#")

		for key, value in self.iter_items():
			lines.append(str(key) + separator + str(value))

		return "\n".join(lines) + ("\n" if lines else "")

	def load(self, filename):
		file_type = self._extension_of(filename)
		if file_type not in self.supported_file_types():
			raise ValueError("Unsupported file type for core Properties: %s" % file_type)
		with open(filename, "r") as handle:
			return self.load_text(handle.read())

	def save(self, filename, comments=None):
		file_type = self._extension_of(filename)
		if file_type not in self.supported_file_types():
			raise ValueError("Unsupported file type for core Properties: %s" % file_type)
		with open(filename, "w") as handle:
			handle.write(self.save_text(comments=comments))
		return True

	def store(self, filename, comments=None):
		return self.save(filename, comments=comments)

	def _extension_of(self, filename):
		name = str(filename).replace("\\", "/")
		dot = name.rfind(".")
		if dot < 0:
			return ""
		return name[dot:].lower()

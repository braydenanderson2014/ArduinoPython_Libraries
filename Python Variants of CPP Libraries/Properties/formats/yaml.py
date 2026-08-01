"""YAML-style key/value Properties support."""

from __future__ import annotations

try:
	from Properties.core import Properties
	from Properties.formats._common import parse_flat_text, serialize_flat_text, strip_quotes
except Exception:
	from core import Properties  # type: ignore[no-redef]
	from _common import parse_flat_text, serialize_flat_text, strip_quotes  # type: ignore[no-redef]


class YamlProperties(Properties):
	SUPPORTED_FILE_TYPES = (".yml", ".yaml")

	@classmethod
	def supported_file_types(cls):
		return cls.SUPPORTED_FILE_TYPES

	def load_text(self, text, clear_first=True):
		if clear_first:
			self.clear()
		mapping = parse_flat_text(text, separators=(":" ,), value_transform=strip_quotes)
		self.from_dict(mapping, clear_first=False)
		return self.elements()

	def save_text(self, comments=None):
		return serialize_flat_text(self.to_dict(), separator=": ", comments=comments)

	def load(self, filename):
		with open(filename, "r") as handle:
			return self.load_text(handle.read())

	def save(self, filename, comments=None):
		with open(filename, "w") as handle:
			handle.write(self.save_text(comments=comments))
		return True

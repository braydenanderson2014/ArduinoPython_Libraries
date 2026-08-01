"""INI-style key/value Properties support."""

from __future__ import annotations

try:
	from Properties.core import Properties
	from Properties.formats._common import parse_flat_text, serialize_flat_text, strip_quotes
except Exception:
	from core import Properties  # type: ignore[no-redef]
	from _common import parse_flat_text, serialize_flat_text, strip_quotes  # type: ignore[no-redef]


class IniProperties(Properties):
	SUPPORTED_FILE_TYPES = (".ini",)

	@classmethod
	def supported_file_types(cls):
		return cls.SUPPORTED_FILE_TYPES

	def load_text(self, text, clear_first=True):
		if clear_first:
			self.clear()

		section = ""
		count = 0
		for raw_line in text.splitlines():
			line = raw_line.strip()
			if not line:
				continue
			if line[0] in self._comment_prefixes:
				continue
			if line.startswith("[") and line.endswith("]"):
				section = line[1:-1].strip()
				continue
			key, value = self._split_line(line, separators=("=", ":"))
			if key is None:
				continue
			key = key.strip()
			if section:
				key = section + "." + key
			self.set_property(key, strip_quotes(value))
			count += 1
		return count

	def save_text(self, comments=None):
		return serialize_flat_text(self.to_dict(), separator=" = ", comments=comments)

	def load(self, filename):
		with open(filename, "r") as handle:
			return self.load_text(handle.read())

	def save(self, filename, comments=None):
		with open(filename, "w") as handle:
			handle.write(self.save_text(comments=comments))
		return True

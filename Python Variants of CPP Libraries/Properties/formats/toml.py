"""TOML-style key/value Properties support."""

from __future__ import annotations

try:
	from Properties.core import Properties
	from Properties.formats._common import strip_quotes
except Exception:
	from core import Properties  # type: ignore[no-redef]
	from _common import strip_quotes  # type: ignore[no-redef]


class TomlProperties(Properties):
	SUPPORTED_FILE_TYPES = (".toml",)

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
			key, value = self._split_line(line, separators=("=",))
			if key is None:
				continue
			key = key.strip()
			if section:
				key = section + "." + key
			self.set_property(key, strip_quotes(value))
			count += 1
		return count

	def save_text(self, comments=None):
		lines = []
		if comments:
			for comment_line in str(comments).splitlines():
				lines.append("# " + comment_line if comment_line else "#")
		current_section = None
		for key, value in self.iter_items():
			section = ""
			name = key
			if "." in key:
				section, name = key.split(".", 1)
			if section != current_section:
				if section:
					lines.append("[" + section + "]")
				current_section = section
			lines.append(str(name) + " = " + str(value))
		return "\n".join(lines) + ("\n" if lines else "")

	def load(self, filename):
		with open(filename, "r") as handle:
			return self.load_text(handle.read())

	def save(self, filename, comments=None):
		with open(filename, "w") as handle:
			handle.write(self.save_text(comments=comments))
		return True

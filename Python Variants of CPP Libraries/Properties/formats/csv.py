"""CSV key/value Properties support."""

from __future__ import annotations

try:
	from Properties.core import Properties
except Exception:
	from core import Properties  # type: ignore[no-redef]


class CsvProperties(Properties):
	SUPPORTED_FILE_TYPES = (".csv",)

	@classmethod
	def supported_file_types(cls):
		return cls.SUPPORTED_FILE_TYPES

	def load_text(self, text, clear_first=True):
		if clear_first:
			self.clear()

		count = 0
		for raw_line in text.splitlines():
			line = raw_line.strip()
			if not line:
				continue
			if line[0] in self._comment_prefixes:
				continue
			if "," not in line:
				continue
			key, value = line.split(",", 1)
			self.set_property(key.strip(), value.strip())
			count += 1
		return count

	def save_text(self, comments=None):
		lines = []
		if comments:
			for comment_line in str(comments).splitlines():
				lines.append("# " + comment_line if comment_line else "#")
		for key, value in self.iter_items():
			lines.append(str(key).replace(",", " ") + "," + str(value).replace("\n", " "))
		return "\n".join(lines) + ("\n" if lines else "")

	def load(self, filename):
		with open(filename, "r") as handle:
			return self.load_text(handle.read())

	def save(self, filename, comments=None):
		with open(filename, "w") as handle:
			handle.write(self.save_text(comments=comments))
		return True

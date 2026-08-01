"""XML key/value Properties support."""

from __future__ import annotations

try:
	from Properties.core import Properties
except Exception:
	from core import Properties  # type: ignore[no-redef]


class XmlProperties(Properties):
	SUPPORTED_FILE_TYPES = (".xml",)

	@classmethod
	def supported_file_types(cls):
		return cls.SUPPORTED_FILE_TYPES

	def load_text(self, text, clear_first=True):
		if clear_first:
			self.clear()

		count = 0
		cursor = 0
		while True:
			entry_start = text.find("<entry", cursor)
			property_start = text.find("<property", cursor)
			if entry_start < 0 and property_start < 0:
				break
			start = entry_start if entry_start >= 0 and (property_start < 0 or entry_start < property_start) else property_start
			key_marker = text.find('key="', start)
			if key_marker < 0:
				cursor = start + 1
				continue
			key_end = text.find('"', key_marker + 5)
			if key_end < 0:
				cursor = start + 1
				continue
			key = text[key_marker + 5:key_end]
			value_start = text.find("", key_end)
			close_tag = text.find("</entry>", key_end)
			if close_tag < 0:
				close_tag = text.find("</property>", key_end)
			if close_tag < 0:
				cursor = key_end + 1
				continue
			value = text[key_end + 2:close_tag].strip()
			self.set_property(key, value)
			count += 1
			cursor = close_tag + 1
		return count

	def save_text(self, comments=None):
		lines = ["<properties>"]
		for key, value in self.iter_items():
			lines.append('  <entry key="' + str(key) + '">' + str(value) + '</entry>')
		lines.append("</properties>")
		return "\n".join(lines) + "\n"

	def load(self, filename):
		with open(filename, "r") as handle:
			return self.load_text(handle.read())

	def save(self, filename, comments=None):
		with open(filename, "w") as handle:
			handle.write(self.save_text(comments=comments))
		return True

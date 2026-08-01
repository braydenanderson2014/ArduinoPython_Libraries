"""JSON key/value Properties support."""

from __future__ import annotations

try:
	import ujson as json
except Exception:
	import json

try:
	from Properties.core import Properties
except Exception:
	from core import Properties  # type: ignore[no-redef]


class JsonProperties(Properties):
	SUPPORTED_FILE_TYPES = (".json",)

	@classmethod
	def supported_file_types(cls):
		return cls.SUPPORTED_FILE_TYPES

	def load_text(self, text, clear_first=True):
		if clear_first:
			self.clear()
		data = json.loads(text)
		if isinstance(data, dict):
			self.from_dict(data, clear_first=False)
		else:
			self.from_dict({}, clear_first=False)
		return self.elements()

	def save_text(self, comments=None):
		mapping = self.to_dict()
		return json.dumps(mapping)

	def load(self, filename):
		with open(filename, "r") as handle:
			return self.load_text(handle.read())

	def save(self, filename, comments=None):
		with open(filename, "w") as handle:
			handle.write(self.save_text(comments=comments))
		return True

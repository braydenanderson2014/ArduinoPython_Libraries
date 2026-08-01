"""MessagePack key/value Properties support.

This module is optional because MessagePack support may not be installed in
minimal Python or MicroPython environments.
"""

from __future__ import annotations

try:
	import msgpack
except Exception:
	msgpack = None

try:
	from Properties.core import Properties
except Exception:
	from core import Properties  # type: ignore[no-redef]


class MsgPackProperties(Properties):
	SUPPORTED_FILE_TYPES = (".msgpack", ".mpk")

	@classmethod
	def supported_file_types(cls):
		return cls.SUPPORTED_FILE_TYPES

	def _require_msgpack(self):
		if msgpack is None:
			raise ImportError("msgpack is not installed in this environment")

	def load_text(self, text, clear_first=True):
		self._require_msgpack()
		if clear_first:
			self.clear()
		data = msgpack.unpackb(text, raw=False)
		if isinstance(data, dict):
			self.from_dict(data, clear_first=False)
		return self.elements()

	def save_text(self, comments=None):
		self._require_msgpack()
		return msgpack.packb(self.to_dict(), use_bin_type=True)

	def load(self, filename):
		self._require_msgpack()
		with open(filename, "rb") as handle:
			payload = handle.read()
		return self.load_text(payload)

	def save(self, filename, comments=None):
		self._require_msgpack()
		with open(filename, "wb") as handle:
			handle.write(self.save_text(comments=comments))
		return True

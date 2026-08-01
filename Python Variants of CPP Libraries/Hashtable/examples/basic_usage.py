"""Basic hashtable usage example."""

from __future__ import annotations

import os
import sys


SCRIPT_DIR = os.path.dirname(__file__)
TABLE_DIR = os.path.dirname(SCRIPT_DIR)
ROOT_DIR = os.path.dirname(TABLE_DIR)

for path in (ROOT_DIR, TABLE_DIR):
	if path not in sys.path:
		sys.path.insert(0, path)

try:
	from Hashtable.core import ArduinoHashTable
except ImportError:
	from core import ArduinoHashTable  # type: ignore[no-redef]


def main() -> None:
	table = ArduinoHashTable(capacity=4, mode="dynamic")
	table.put("temp", 25)
	table.put("humid", 60)

	print("temp:", table.get("temp"))
	print("humid:", table.get("humid"))
	print("missing:", table.get("missing", default=-1))
	print("optional missing:", table.get_optional("missing").or_else(-1))


if __name__ == "__main__":
	main()

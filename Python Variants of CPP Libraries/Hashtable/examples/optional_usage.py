"""Optional-value helper example."""

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
	table.put("present", 123)

	present = table.get_optional("present")
	missing = table.get_optional("missing")

	print("present has value:", present.has_value())
	print("present value:", present.get_value())
	print("missing has value:", missing.has_value())
	print("missing or_else:", missing.or_else(-1))


if __name__ == "__main__":
	main()

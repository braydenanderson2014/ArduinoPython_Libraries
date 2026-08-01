"""Sorting helper example."""

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
	from Hashtable.sorting import SortingHashtable
except ImportError:
	from sorting import SortingHashtable  # type: ignore[no-redef]


def main() -> None:
	table = SortingHashtable()
	table.put("delta", 4)
	table.put("alpha", 1)
	table.put("charlie", 3)
	table.put("bravo", 2)

	print("sorted keys:", table.sorted_keys())
	print("sorted items:", table.sorted_items())


if __name__ == "__main__":
	main()
